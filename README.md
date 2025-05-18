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

Instalação e Uso
Para configurar e executar o Assistent de Receitas Domésticas na sua máquina, siga os passos abaixo:

Pré-requisitos
Python 3.7+: Certifique-se de ter uma versão compatível do Python instalada. Você pode baixar em python.org.

Git: Necessário para clonar o repositório. Baixe em git-scm.com.

Chaves de API do Google Gemini e Google Text-to-Speech: Você precisará obter credenciais para acessar as APIs do Google Cloud. Consulte a documentação oficial do Google Cloud para saber como gerar chaves de API para esses serviços.

Passos para Instalação
Clone o Repositório:
Abra o terminal ou prompt de comando e clone o repositório para a sua máquina local:

git clone https://github.com/Caro-cyber/sistema-iareceita.git

Navegue até o Diretório do Projeto:
Entre na pasta do projeto clonado:

cd sistema-iareceita

Crie um Ambiente Virtual (Recomendado):
É uma boa prática criar um ambiente virtual para isolar as dependências do projeto.

# Para Python 3
python -m venv venv

Ative o Ambiente Virtual:

No Windows:

.\venv\Scripts\activate

No macOS e Linux:

source venv/bin/activate

Você verá (venv) no início da linha de comando, indicando que o ambiente virtual está ativo.

Instale as Dependências:
Este projeto dependerá de bibliotecas para interagir com as APIs do Google e possivelmente para PNL. Assumindo que haja um arquivo requirements.txt na raiz do projeto (você precisará criá-lo e listar as bibliotecas usadas, como google-generativeai, google-cloud-texttospeech, etc.), instale-as com pip:

pip install -r requirements.txt

(Se o arquivo requirements.txt ainda não existir, você precisará instalá-las manualmente com pip install nome_da_biblioteca).

Configure suas Chaves de API:
As chaves de API para o Google Gemini e Google Text-to-Speech precisam ser configuradas para que o script possa se autenticar e usar os serviços. A forma mais segura e comum é usar variáveis de ambiente.

Crie um arquivo .env na raiz do projeto (se ele não existir) e adicione suas chaves:

# Exemplo de arquivo .env
GOOGLE_API_KEY_GEMINI="SUA_CHAVE_API_GOOGLE_GEMINI"
GOOGLE_API_KEY_TTS="SUA_CHAVE_API_GOOGLE_TTS"
# Outras variáveis de ambiente se necessário

(Você precisará garantir que o código Python lê essas variáveis de ambiente, por exemplo, usando a biblioteca python-dotenv e configurando as chamadas às APIs do Google para usar essas chaves).

Como Executar
Após seguir os passos de instalação e configurar suas chaves de API, você pode executar o script principal do assistente.

Assumindo que o ponto de entrada do seu assistente seja um arquivo Python (por exemplo, main.py ou assistant.py), execute-o com o Python:

python seu_arquivo_principal.py

O assistente deverá iniciar no terminal (ou na interface que você desenvolver) e solicitar os ingredientes.

Lembre-se que estas são instruções genéricas. Conforme você desenvolve o projeto e adiciona as implementações reais das APIs e da interface, precisará refinar e detalhar estas instruções no seu README.md.

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
