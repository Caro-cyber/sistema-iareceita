# Assistente de Receitas com IA

Um assistente de receitas que utiliza IA para sugerir receitas baseadas nos ingredientes disponíveis, com recursos de áudio e perguntas interativas.

## Funcionalidades

- 🔍 Busca de receitas por ingredientes disponíveis
- 🗣️ Geração de áudio para instruções de preparo
- ❓ Sistema de perguntas e respostas sobre as receitas
- 🔄 Interface interativa e responsiva

## Tecnologias Utilizadas

- Python 3.8+
- Flask
- Google Gemini AI
- Google Cloud Text-to-Speech
- HTML/CSS/JavaScript

## Configuração do Ambiente

1. Clone o repositório:
```bash
git clone [URL_DO_SEU_REPOSITORIO]
cd [NOME_DO_DIRETORIO]
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
Crie um arquivo `.env` na raiz do projeto com:
```
GEMINI_API_KEY=sua_chave_api_gemini
GOOGLE_APPLICATION_CREDENTIALS=caminho/para/seu/arquivo-credenciais.json
```

## Executando o Projeto

1. Ative o ambiente virtual (se ainda não estiver ativo)
2. Execute o servidor Flask:
```bash
python app.py
```
3. Acesse http://localhost:5000 no seu navegador

## Estrutura do Projeto

```
.
├── app.py                   # Lógica principal do Flask, rotas
├── services/               # Módulos de serviço
│   ├── __init__.py
│   ├── gemini_service.py   # Interação com Google Gemini
│   ├── tts_service.py      # Interação com Google Text-to-Speech
│   └── ingredient_service.py # Processamento de ingredientes
├── templates/              # Arquivos HTML (Jinja2)
│   ├── index.html
├── static/                # Arquivos estáticos
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── script.js
│   └── audio/            # Onde os áudios gerados são salvos temporariamente
└── requirements.txt      # Dependências Python
```

## Contribuindo

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes. 