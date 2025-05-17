# services/ingredient_service.py
import re

def normalize_ingredient(name):
    name = name.lower().strip()
    # Adicionar mais regras de normalização se necessário (ex: plural para singular)
    # Exemplo simples de sinônimos (pode ser expandido para um dict maior ou DB)
    sinonimos = {
        "cebola roxa": "cebola",
        "batata inglesa": "batata",
        "tomate italiano": "tomate"
    }
    return sinonimos.get(name, name)

def process_ingredients_input(ingredients_str):
    """
    Processa a string de ingredientes fornecida pelo usuário.
    Assume ingredientes separados por vírgula ou nova linha.
    """
    # Separa por vírgula ou nova linha, remove espaços extras e itens vazios
    ingredients = re.split(r'[,\n]', ingredients_str)
    processed_ingredients = set() # Usar set para remover duplicatas automaticamente

    for ing in ingredients:
        if ing.strip(): # Ignora strings vazias
            normalized_ing = normalize_ingredient(ing.strip())
            processed_ingredients.add(normalized_ing)
    return list(processed_ingredients)

# Exemplo de uso:
# raw_input = "Tomate, Cebola roxa, Batata inglesa, tomate  "
# print(process_ingredients_input(raw_input))
# Output: ['tomate', 'cebola', 'batata'] 