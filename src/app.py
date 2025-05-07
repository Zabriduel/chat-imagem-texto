import streamlit as st
import os
import dotenv
import google.generativeai as genai
import base64
from PIL import Image
from io import BytesIO
import requests
from pathlib import Path

# Configuração inicial
st.set_page_config(page_title="🔥 Rengoku AI Generator", layout="wide", page_icon="🔥")
dotenv.load_dotenv()

current_dir = Path(__file__).parent

def load_css():
    css_path = current_dir / "style.css"
    if css_path.exists():
        with open(css_path, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def set_background():
    bg_path = current_dir / "background.webp"
    if bg_path.exists():
        with open(bg_path, "rb") as f:
            bg_base64 = base64.b64encode(f.read()).decode()
        st.markdown(f"""
            <style>
                .stApp {{
                    background-image: url(data:image/webp;base64,{bg_base64});
                    background-size: cover;
                    background-position: center center;
                    background-repeat: no-repeat;
                    background-attachment: fixed;
                }}
            </style>
        """, unsafe_allow_html=True)

def validate_api_key(api_key, provider):
    if provider == "Google" and api_key and not api_key.startswith("AIza"):
        st.error("❌ A chave da API do Google deve começar com 'AIza'")
        return False
    if provider == "Stability" and api_key and not api_key.startswith("sk-"):
        st.error("❌ A chave da API do Stability.ai deve começar com 'sk-'")
        return False
    return True

def translate_with_gemini(text, api_key):
    try:
        if not text.strip():
            return text
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("models/gemini-1.5-flash")
        response = model.generate_content(
            f"Por favor, traduza este prompt de geração de imagem para inglês "
            f"mantendo fielmente o significado e estilo artístico: '{text}'\n\n"
            f"Retorne APENAS a tradução em inglês, sem comentários ou explicações."
        )
        translated = response.text.strip().replace('"', '')
        return translated or text
    except Exception as e:
        st.warning(f"⚠️ Não foi possível traduzir o prompt. Erro: {str(e)}")
        return text

def generate_gemini_content(prompt, api_key):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("models/gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response
    except Exception as e:
        st.error(f"🚨 Erro no Gemini: {str(e)}")
        return None

def generate_stability_image(prompt, api_key, gemini_key=None):
    try:
        needs_translation = any(char.lower() in 'áéíóúâêîôûãõç' for char in prompt)
        english_prompt = translate_with_gemini(prompt, gemini_key) if gemini_key and needs_translation else prompt
        if english_prompt != prompt:
            st.success(f"🌐 Tradução para inglês:\n{english_prompt}")
        url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        payload = {
            "text_prompts": [{"text": english_prompt, "weight": 1}],
            "cfg_scale": 7,
            "height": 1024,
            "width": 1024,
            "samples": 1,
            "steps": 30,
            "style_preset": "enhance"
        }
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code != 200:
            st.error(f"🚨 Erro na API Stability.ai (Código {response.status_code}): {response.json().get('message', 'Erro desconhecido')}")
            return None
        result = response.json()
        if not result.get("artifacts"):
            st.error("❌ Nenhuma imagem foi retornada pela API.")
            return None
        img_data = base64.b64decode(result["artifacts"][0]["base64"])
        return Image.open(BytesIO(img_data))
    except Exception as e:
        st.error(f"🚨 Erro inesperado ao gerar imagem: {str(e)}")
        return None

def add_logo():
    logo_path = current_dir / "rengoku_icon.png"
    if logo_path.exists():
        with open(logo_path, "rb") as f:
            logo_base64 = base64.b64encode(f.read()).decode()
        st.markdown(f"""
            <style>
                [data-testid="stSidebarNav"] {{
                    background-image: url(data:image/png;base64,{logo_base64});
                    background-repeat: no-repeat;
                    background-position: 20px 20px;
                    background-size: 80%;
                }}
            </style>
        """, unsafe_allow_html=True)

def main():
    load_css()
    set_background()
    add_logo()

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "mode" not in st.session_state:
        st.session_state.mode = "Texto (Gemini)"

    st.markdown("""
    <div class="header-container">
        <h1>🔥 Rengoku AI Generator</h1>
        <p>"Defenda o que você acredita com todo o seu coração!"<br>– Kyojuro Rengoku</p>
    </div>
""", unsafe_allow_html=True)


    st.markdown("---")

    with st.sidebar:
        st.header("⚙️ Opções")
        if "sidebar_open" not in st.session_state:
            st.session_state.sidebar_open = True
        st.session_state.sidebar_open = st.checkbox("Exibir configurações avançadas", value=st.session_state.sidebar_open)

        if st.session_state.sidebar_open:
            style_options = {
                "Aprimorado": "enhance",
                "Anime": "anime",
                "Fotográfico": "photographic",
                "Arte Fantástica": "fantasy-art",
                "Isométrico": "isometric",
                "Modelo 3D": "3d-model",
                "Pixel Art": "pixel-art"
            }
            selected_label = st.selectbox("🎨 Estilo da Imagem", list(style_options.keys()), index=0)
            st.session_state.image_style = style_options[selected_label]

            st.session_state.text_style = st.selectbox(
                "📝 Estilo de Escrita",
                ["normal", "formal", "poético", "motivacional", "narrativa", "dramática"],
                index=0
            )

    gemini_key = os.getenv("GEMINI_API_KEY")
    stability_key = os.getenv("STABILITY_API_KEY")

    if not gemini_key or not validate_api_key(gemini_key, "Google") or not stability_key or not validate_api_key(stability_key, "Stability"):
        with st.expander("🔧 Configuração das APIs", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                gemini_key = st.text_input("Google Gemini Key (AIza...):", type="password")
            with col2:
                stability_key = st.text_input("Stability.ai Key (sk-...):", type="password")

    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f"<b class='user-message'>🧑‍💻 Você:</b><br>{message['content']}", unsafe_allow_html=True)
        else:
            if message["type"] == "text":
                rengoku_icon_path = current_dir / "rengoku_icon.png"
                if rengoku_icon_path.exists():
                    with open(rengoku_icon_path, "rb") as f:
                        rengoku_icon_base64 = base64.b64encode(f.read()).decode()
                    icon_html = f'<img src="data:image/png;base64,{rengoku_icon_base64}" width="24" style="vertical-align: middle; margin-right: 6px;">'
                else:
                    icon_html = "🔥"
                st.markdown(f"<b class='assistant-message'>{icon_html}Rengoku:</b><br>{message['content']}", unsafe_allow_html=True)
            elif message["type"] == "image":
                st.image(message["content"], width=500)
                buffered = BytesIO()
                message["content"].save(buffered, format="PNG")
                st.download_button("📥 Baixar imagem", data=buffered.getvalue(), file_name="rengoku_gerada.png", mime="image/png")

    with st.container():
        col1, col2 = st.columns([4, 1])
        with col1:
            user_input = st.chat_input("Digite seu prompt aqui...")
        with col2:
            st.session_state.mode = st.selectbox(
                "Modo",
                ["Texto (Gemini)", "Imagem (Stability.ai)"],
                index=0 if st.session_state.mode == "Texto (Gemini)" else 1,
                label_visibility="collapsed"
            )

    if user_input:
        st.session_state.chat_history.append({
            "role": "user",
            "type": "text",
            "content": user_input
        })
        st.rerun()

    if st.session_state.chat_history and st.session_state.chat_history[-1]["role"] == "user":
        last_user_message = st.session_state.chat_history[-1]["content"]

        with st.spinner("⏳ Processando..."):
            if st.session_state.mode == "Texto (Gemini)":
                if not gemini_key:
                    st.error("❌ Por favor, forneça a chave do Google Gemini")
                    st.stop()

                style = st.session_state.get("text_style", "normal")
                prompt = f"Escreva no estilo {style}:\n{last_user_message}" if style != "normal" else last_user_message

                response = generate_gemini_content(prompt, gemini_key)
                result = response.text if response else "Erro ao gerar resposta."

                st.session_state.chat_history.append({
                    "role": "assistant",
                    "type": "text",
                    "content": result
                })
                st.rerun()

            elif st.session_state.mode == "Imagem (Stability.ai)":
                if not stability_key:
                    st.error("❌ Por favor, forneça a chave do Stability.ai")
                    st.stop()

                style = st.session_state.get("image_style", "enhance")
                prompt = f"{last_user_message} (style: {style})"

                img = generate_stability_image(prompt, stability_key, gemini_key)
                if img:
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "type": "image",
                        "content": img
                    })
                else:
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "type": "text",
                        "content": "❌ Erro ao gerar imagem."
                    })
                st.rerun()

if __name__ == "__main__":
    main()
