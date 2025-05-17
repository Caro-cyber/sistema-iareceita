from flask import Flask, render_template, request, jsonify, url_for
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do .env
load_dotenv()

# Importar os módulos de serviço
from services import ingredient_service, gemini_service, tts_service

app = Flask(__name__)
app.secret_key = os.urandom(24) # Para flash messages ou sessões futuras

# Armazenamento em memória para receitas (simples, para evitar chamadas repetidas ao Gemini para a mesma sessão)
# Em produção, isso poderia ser um cache mais robusto (Redis) ou um banco de dados.
# A chave será uma tupla de ingredientes (ordenada), o valor será a lista de receitas.
# Ou, mais simples para este exemplo, apenas a última receita gerada.
current_recipes_cache = {} # { "recipe_id": recipe_data, ... }

# Inicialização dos serviços
with app.app_context():
    """Inicializa os clientes das APIs do Google."""
    print("Inicializando serviços...")
    gemini_service.init_gemini_model()
    tts_service.init_tts_client()
    # Verificar se as chaves de API estão carregadas
    if not os.getenv("GEMINI_API_KEY"):
        print("AVISO: GEMINI_API_KEY não está configurada no .env!")
    if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        print("AVISO: GOOGLE_APPLICATION_CREDENTIALS não está configurada no .env (necessário para TTS)!")


@app.route('/', methods=['GET'])
def index():
    """Página inicial para inserir ingredientes."""
    return render_template('index.html')

@app.route('/get_recipes', methods=['POST'])
def get_recipes():
    """Recebe ingredientes, busca receitas e retorna como JSON."""
    global current_recipes_cache
    current_recipes_cache.clear() # Limpa cache de receitas anteriores

    data = request.get_json()
    if not data or 'ingredients' not in data:
        return jsonify({"error": "Nenhum ingrediente fornecido."}), 400

    raw_ingredients_str = data['ingredients']
    processed_ingredients = ingredient_service.process_ingredients_input(raw_ingredients_str)

    if not processed_ingredients:
        return jsonify({"error": "Ingredientes inválidos ou vazios após processamento."}), 400

    print(f"Ingredientes processados para Gemini: {processed_ingredients}")
    
    # Chama o Gemini Service
    recipes_data = gemini_service.find_recipes_with_gemini(processed_ingredients)

    if isinstance(recipes_data, dict) and "error" in recipes_data:
        return jsonify(recipes_data), 500 # Erro do Gemini

    # Armazena as receitas no cache para acesso posterior (TTS, detalhes)
    for recipe in recipes_data:
        current_recipes_cache[recipe['id']] = recipe
        
    return jsonify({"recipes": recipes_data})


@app.route('/get_recipe_audio/<recipe_id>', methods=['GET'])
def get_recipe_audio(recipe_id):
    """Gera áudio para as instruções de uma receita específica."""
    if recipe_id not in current_recipes_cache:
        return jsonify({"error": "Receita não encontrada ou sessão expirada."}), 404

    recipe = current_recipes_cache[recipe_id]
    instructions_text = recipe.get("instructions_text", "")

    if not instructions_text:
        return jsonify({"error": "Instruções não disponíveis para esta receita."}), 404

    # Nome do arquivo de áudio baseado no ID da receita (para evitar colisões e facilitar a limpeza)
    # Adicionar um hash ou timestamp se quiser garantir unicidade absoluta entre sessões
    audio_filename_no_ext = f"recipe_audio_{recipe_id.replace(' ', '_')}"
    
    relative_audio_path = tts_service.generate_audio_instructions(instructions_text, audio_filename_no_ext)

    if relative_audio_path:
        # url_for gera o caminho completo para o arquivo estático
        audio_url = url_for('static', filename=relative_audio_path, _external=False) # _external=False para caminho relativo
        return jsonify({"audio_url": audio_url})
    else:
        return jsonify({"error": "Falha ao gerar áudio."}), 500

@app.route('/ask_question/<recipe_id>', methods=['POST'])
def ask_question_to_gemini(recipe_id):
    if recipe_id not in current_recipes_cache:
        return jsonify({"error": "Receita não encontrada ou sessão expirada."}), 404

    recipe = current_recipes_cache[recipe_id]
    data = request.get_json()
    question = data.get('question')

    if not question:
        return jsonify({"error": "Nenhuma pergunta fornecida."}), 400

    # Construir um contexto simples para o Gemini
    recipe_context = f"Nome da Receita: {recipe.get('name', 'N/A')}\n"
    recipe_context += f"Ingredientes: {recipe.get('ingredients_text', 'N/A')}\n"
    recipe_context += f"Modo de Preparo: {recipe.get('instructions_text', 'N/A')}\n"

    answer_data = gemini_service.ask_follow_up_question(recipe_context, question)
    
    if "error" in answer_data:
        return jsonify(answer_data), 500
    
    return jsonify(answer_data)


if __name__ == '__main__':
    # Certifique-se de que a pasta static/audio exista
    if not os.path.exists("static/audio"):
        os.makedirs("static/audio")
    app.run(debug=True, host='0.0.0.0', port=5000) # debug=True para desenvolvimento 