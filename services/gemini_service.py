# services/gemini_service.py
import google.generativeai as genai
import os
import re

# Configurar a API Key (idealmente via variável de ambiente)
# genai.configure(api_key=os.environ["GEMINI_API_KEY"])
# Ou diretamente, mas menos seguro para código compartilhado:
# genai.configure(api_key="SUA_API_KEY_AQUI")

# Modelo de Geração
generation_config = {
    "temperature": 0.7, # Ajuste para mais criatividade ou mais factualidade
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048, # Ajuste conforme necessidade
}
safety_settings = [ # Ajuste os níveis de segurança
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = None # Será inicializado em app.py ou na primeira chamada

def init_gemini_model():
    global model
    if model is None:
        try:
            api_key = os.environ.get("GEMINI_API_KEY")
            if not api_key:
                raise ValueError("GEMINI_API_KEY não encontrada nas variáveis de ambiente.")
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash-latest", # Ou outro modelo apropriado
                generation_config=generation_config,
                safety_settings=safety_settings
            )
            print("Modelo Gemini inicializado com sucesso.")
        except Exception as e:
            print(f"Erro ao inicializar o modelo Gemini: {e}")
            model = None # Garante que o modelo não seja usado se a inicialização falhar
    return model

def find_recipes_with_gemini(ingredients_list):
    """
    Usa o Gemini para encontrar/gerar receitas com base nos ingredientes.
    """
    if not model:
        print("Modelo Gemini não inicializado.")
        return {"error": "Modelo Gemini não disponível."}

    if not ingredients_list:
        return {"error": "Nenhum ingrediente fornecido."}

    ingredients_str = ", ".join(ingredients_list)
    prompt = f"""
    Você é um assistente de culinária.
    Quero sugestões de receitas que usem principalmente os seguintes ingredientes: {ingredients_str}.
    Por favor, me forneça 2 ou 3 sugestões de receitas.
    Para cada receita, inclua:
    1. Nome da Receita (coloque entre **Nome da Receita:** e **Ingredientes:**)
    2. Ingredientes (liste todos, incluindo os que eu não mencionei, mas que são necessários, marque os que eu forneci com um asterisco (*) ao lado. Formato: - Item (quantidade opcional) [*])
    3. Modo de Preparo (passos numerados)

    Exemplo de formato para uma receita:
    **Nome da Receita:** Omelete Simples
    **Ingredientes:**
    - Ovos (2 unidades) [*]
    - Sal (a gosto)
    - Pimenta do reino (a gosto)
    - Óleo ou manteiga (para untar)
    **Modo de Preparo:**
    1. Bata os ovos em uma tigela.
    2. Tempere com sal e pimenta.
    3. Aqueça uma frigideira com óleo ou manteiga.
    4. Despeje os ovos batidos e cozinhe até firmar.

    --- (use três hífens para separar múltiplas receitas, se houver)
    """

    try:
        response = model.generate_content(prompt)
        # Adicionar logging da resposta bruta pode ser útil para depuração
        # print("Resposta bruta do Gemini:", response.text)
        return parse_gemini_recipes(response.text)
    except Exception as e:
        print(f"Erro ao chamar a API Gemini: {e}")
        # Retornar a mensagem de erro pode ser útil no frontend
        return {"error": f"Erro ao gerar receitas: {str(e)}"}

def parse_gemini_recipes(gemini_response_text):
    """
    Analisa a resposta de texto do Gemini para extrair múltiplas receitas.
    Esta função precisará de ajustes finos baseados no formato real da saída do Gemini.
    """
    recipes = []
    # Tenta dividir por um separador claro entre receitas, como "---"
    raw_recipes = gemini_response_text.split("\n---\n")

    for i, raw_recipe in enumerate(raw_recipes):
        if not raw_recipe.strip():
            continue

        name_match = re.search(r"\*\*Nome da Receita:\*\*\s*(.*?)\s*\*\*Ingredientes:\*\*", raw_recipe, re.DOTALL | re.IGNORECASE)
        ingredients_match = re.search(r"\*\*Ingredientes:\*\*\s*(.*?)\s*\*\*Modo de Preparo:\*\*", raw_recipe, re.DOTALL | re.IGNORECASE)
        instructions_match = re.search(r"\*\*Modo de Preparo:\*\*\s*(.*)", raw_recipe, re.DOTALL | re.IGNORECASE)

        if name_match and ingredients_match and instructions_match:
            recipe_name = name_match.group(1).strip()
            ingredients_text = ingredients_match.group(1).strip()
            instructions_text = instructions_match.group(1).strip()

            recipes.append({
                "id": f"recipe_{i}", # ID simples para uso no frontend
                "name": recipe_name,
                "ingredients_text": ingredients_text, # Mantém o formato do Gemini por enquanto
                "instructions_text": instructions_text # Mantém o formato do Gemini
            })
        else:
            # Se a análise falhar para uma receita, podemos logar ou adicionar como "não processada"
            print(f"Não foi possível parsear a receita: {raw_recipe[:100]}...")
            recipes.append({
                "id": f"unparsed_recipe_{i}",
                "name": f"Receita não processada {i+1}",
                "raw_text": raw_recipe.strip() # Para depuração
            })


    if not recipes and gemini_response_text.strip(): # Se não houve split, mas há texto
        # Tentar um fallback para uma única receita, caso o separador "---" não seja usado
        # ou se apenas uma receita for retornada sem o separador.
        name_match = re.search(r"\*\*Nome da Receita:\*\*\s*(.*?)\s*\*\*Ingredientes:\*\*", gemini_response_text, re.DOTALL | re.IGNORECASE)
        ingredients_match = re.search(r"\*\*Ingredientes:\*\*\s*(.*?)\s*\*\*Modo de Preparo:\*\*", gemini_response_text, re.DOTALL | re.IGNORECASE)
        instructions_match = re.search(r"\*\*Modo de Preparo:\*\*\s*(.*)", gemini_response_text, re.DOTALL | re.IGNORECASE)
        if name_match and ingredients_match and instructions_match:
             recipes.append({
                "id": "recipe_0",
                "name": name_match.group(1).strip(),
                "ingredients_text": ingredients_match.group(1).strip(),
                "instructions_text": instructions_match.group(1).strip()
            })

    return recipes


def ask_follow_up_question(recipe_context, question):
    """
    Envia uma pergunta de acompanhamento para o Gemini sobre uma receita específica.
    """
    if not model:
        print("Modelo Gemini não inicializado.")
        return {"error": "Modelo Gemini não disponível."}

    prompt = f"""
    Contexto da Receita:
    {recipe_context}

    Pergunta do usuário: {question}

    Por favor, responda à pergunta do usuário com base no contexto da receita fornecido.
    Se a pergunta for sobre substituições de ingredientes, seja específico.
    Se for sobre tempo, tente estimar.
    """
    try:
        response = model.generate_content(prompt)
        return {"answer": response.text.strip()}
    except Exception as e:
        print(f"Erro ao chamar a API Gemini para pergunta de acompanhamento: {e}")
        return {"error": f"Erro ao processar a pergunta: {str(e)}"} 