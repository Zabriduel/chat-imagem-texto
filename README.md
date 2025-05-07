# 🔥 Rengoku AI Generator
*"Se estiver se sentindo desmotivados ou sentindo que não é bom o suficiente incendeie 🔥 o seu coração💓!"* – Kyojuro Rengoku

Este é um chatbot de inteligência artificial criado com Streamlit, que permite ao usuário gerar textos estilizados com o Google Gemini ou imagens incríveis com a API da Stability.ai. O projeto é inspirado no personagem Kyojuro Rengoku do anime *Demon Slayer*, e toda a estética da aplicação reflete sua energia vibrante e visual icônico.

## 🚀 Funcionalidades
- 💬 Geração de texto com Google Gemini 1.5 Flash
- 🌐 Tradução automática de prompts em português para inglês
- 🎨 Estilização personalizada para texto e imagem
- 📜 Histórico de conversa com visual diferenciado
- 💡 Interface estilizada com CSS temático (Rengoku)
- 🔒 Uso de `.env` para armazenamento seguro das chaves de API

## 📂 Estrutura de Pastas 
```bash
📦 rengoku-ai-generator/
├── app.py                  # Código principal da aplicação Streamlit
├── style.css               # Arquivo de estilização com tema inspirado em Rengoku
├── background.webp         # Imagem de fundo da interface
├── rengoku_icon.png        # Ícone do personagem Rengoku usado no chat
├── .gitignore              # Ignora o .env e diretórios como venv
├── requirements.txt        # Dependências do projeto
└── README.md               # Este arquivo
```

## ⚙️ Como Executar Localmente

1. Clone este repositório:

    ```bash
    git clone https://github.com/Zabriduel/chat-imagem-texto.git
    cd chat-imagem-texto.git
    ```

2. Crie e ative um ambiente virtual (opcional, mas recomendado):

    ```bash
    python -m venv venv
    source venv/bin/activate  # ou venv\Scripts\activate no Windows
    ```

3. Instale as dependências:

    ```bash
    pip install -r requirements.txt
    ```

4. Crie um arquivo `.env` com as seguintes variáveis:

    ```env
    GEMINI_API_KEY=AIza...       # Chave da API do Google Gemini
    STABILITY_API_KEY=sk-...     # Chave da API da Stability.ai
    ```

5. Execute o app:

    ```bash
    streamlit run app.py
    ```

## 🧠 Tecnologias Usadas
- Python 3.10+
- Streamlit
- Google Generative AI (Gemini)
- Stability.ai API
- Requests
- PIL (Pillow)
- dotenv

## 🎨 Estilo Visual

O visual foi inspirado no Hashira das Chamas, Rengoku, do anime *Demon Slayer*. Cores, fontes e ícones remetem ao seu estilo marcante. A interface usa elementos como:

- 🔥 Fundo com imagem temática
- 🟠 Paleta de cores quente e vibrante
- 🖌️ Fontes estilizadas e sombras
- 📦 Sidebar com logo personalizado

## 🛡️ Segurança

As chaves de API são carregadas de um `.env` local.

O arquivo `.gitignore` evita o upload de dados sensíveis como `.env` e `venv/`.

## 🤝 Contribuições

Sinta-se à vontade para contribuir com melhorias, correções ou novos estilos! Abra um pull request ou envie sugestões via issues.

