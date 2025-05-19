import os
import whisper
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st
import yt_dlp
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
LLM_AVAILABLE = bool(GOOGLE_API_KEY)

if not LLM_AVAILABLE:
    st.warning(
        "Chave da API do Google (GOOGLE_API_KEY) não encontrada no ambiente ou arquivo .env. "
        "A funcionalidade de reformatação da transcrição pela IA será desabilitada. "
        "A transcrição bruta será fornecida."
    )
    # Não paramos o app, apenas desabilitamos a reformatação por IA.

AUDIO_FILENAME_BASE = "downloaded_audio"

@st.cache_resource
def load_whisper_model():
    """Carrega o modelo Whisper."""
    return whisper.load_model("base")

whisper_model = load_whisper_model()

@st.cache_resource
def load_llm():
    """Carrega o modelo de linguagem generativa do Google, se a API key estiver disponível."""
    if GOOGLE_API_KEY:
        return ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GOOGLE_API_KEY)
    return None

llm = load_llm() if LLM_AVAILABLE else None

reformat_prompt_template_text = (
    "Você é um assistente especialista em processamento de texto. "
    "Sua tarefa é pegar a transcrição de um áudio e reformatá-la em tópicos (bullet points) usando Markdown. "
    "O objetivo é organizar a informação de forma clara, concisa e fácil de ler, sem perder NENHUM detalhe ou informação do texto original. "
    "Mantenha a linguagem e o tom do texto original. "
    "Se houver diálogos ou diferentes falantes, tente representá-los de forma clara dentro da estrutura de tópicos, se possível (ex: usando sub-tópicos ou indicando o falante). "
    "Não adicione introduções, saudações, despedidas ou conclusões que não estejam explicitamente no texto original. Apenas reformate o conteúdo fornecido. "
    "Certifique-se de que cada ponto da lista seja informativo e represente uma parte do conteúdo original.\n\n"
    "Texto Original:\n"
    "------------\n"
    "{transcricao_bruta}\n"
    "------------\n\n"
    "Texto Reformatado em Tópicos (Markdown):\n"
)
reformat_prompt = ChatPromptTemplate.from_template(reformat_prompt_template_text)

def download_audio_from_youtube(url, output_filename=AUDIO_FILENAME_BASE):
    """Baixa o áudio de uma URL do YouTube como MP3."""
    output_template = os.path.splitext(output_filename)[0]
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': output_template,
        'noplaylist': True,
        'quiet': True,
        'ffmpeg_location': '/usr/bin/ffmpeg',
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            st.info(f"Baixando áudio de: {url}...")
            ydl.download([url])
        if os.path.exists(output_filename):
            st.success("Áudio baixado com sucesso!")
            return output_filename
        else:
            st.error(f"Arquivo de áudio esperado ({output_filename}) não encontrado após o download.")
            return None
    except Exception as e:
        st.error(f"Erro ao baixar o áudio: {e}")
        return None

def transcribe_audio(audio_path):
    """Transcreve o áudio usando o modelo Whisper."""
    st.info("Transcrevendo áudio... Isso pode levar alguns minutos.")
    result = whisper_model.transcribe(audio_path)
    st.success("Áudio transcrito com sucesso!")
    return result["text"]


# Streamlit UI Styling
st.markdown(
    """
    <style>
    /* Define o fundo roxo escuro para toda a página */
    .stApp {
        background-color: #88185D !important;
    }

    /* Personaliza o título */
    h1, h2, h3 {
        color: #FFA21C !important;
        text-align: center;
    }

    /* Personaliza os botões */
    div.stButton > button:first-child {
        background-color: #FFA21C !important;
        color: white !important;
        font-size: 18px;
        border-radius: 8px;
        border: 2px solid white;
        padding: 10px 24px;
    }
    div.stButton > button:first-child:hover {
        background-color: #FF8C00 !important;
    }

    /* Personaliza os inputs */
    div.stTextInput > label {
        font-size: 18px;
        font-weight: bold;
        color: #FFA21C !important;
    }

    /* Personaliza a área do chat */
    div.stChatMessage {
        background-color: #5C1042 !important;
        border-radius: 8px;
        padding: 10px;
    }

    /* Personaliza os textos gerais */
    body, p, div {
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Sidebar ---
# st.sidebar.image("logo-UNIRUY-Branco.png", width=350)
st.sidebar.header("OneScriber")
st.sidebar.markdown("Transcrição de YouTube com IA e Chat Interativo")
st.sidebar.markdown("Desenvolvido por Vítor Em.")
st.sidebar.markdown("<a href='https://github.com/vitorpq' target='_blank'>GitHub</a>", unsafe_allow_html=True)

# --- Main Page ---
st.title("🎧 OneScriber 💬")

# --- Session State Initialization ---
if "transcription_text" not in st.session_state:
    st.session_state.transcription_text = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "chain" not in st.session_state:
    st.session_state.chain = reformat_prompt | llm

# --- YouTube URL Input and Transcription ---
youtube_url = st.text_input("Insira a URL do vídeo do YouTube:", key="youtube_url_input")

if st.button("Transcrever Áudio e Preparar Chat", key="transcribe_button"):
    if youtube_url:
        st.session_state.transcription_text = None
        st.session_state.chat_history = [] # Reseta o histórico do chat para nova transcrição
        
        if os.path.exists(AUDIO_FILENAME_BASE):
            try:
                os.remove(AUDIO_FILENAME_BASE)
            except OSError as e:
                st.warning(f"Não foi possível remover o arquivo de áudio antigo: {e}")

        audio_file_path = download_audio_from_youtube(youtube_url)
        if audio_file_path:
            transcribed_text = transcribe_audio(audio_file_path)
            if transcribed_text:
                st.session_state.transcription_text = transcribed_text
                final_text_for_download = transcribed_text
                if llm and reformat_prompt:
                    st.info("Reformatando a transcrição com IA (Gemini)... Isso pode levar um momento.")
                    try:
                        reformat_chain = reformat_prompt | llm
                        response = reformat_chain.invoke({"transcricao_bruta": transcribed_text})
                        reformatted_content = response.content
                        if reformatted_content:
                            final_text_for_download = reformatted_content
                            st.session_state.transcription_text = reformatted_content # Atualiza com o texto reformatado
                            st.success("Transcrição reformatada pela IA com sucesso!")
                        else:
                            st.warning("A IA retornou um conteúdo vazio. Usando a transcrição bruta.")
                    except Exception as e:
                        st.error(f"Erro ao reformatar com IA: {e}. Usando a transcrição bruta.")
                elif not LLM_AVAILABLE:
                    st.info("Reformatação por IA desabilitada (API Key não configurada). Usando transcrição bruta.")
                try:
                    with open("transcription.txt", "w", encoding="utf-8") as f:
                        f.write(transcribed_text)
                    st.info("Transcrição salva em transcription.txt")
                except Exception as e:
                    st.warning(f"Não foi possível salvar o arquivo de transcrição: {e}")
                
                st.subheader("Transcrição do Áudio:")
                st.text_area("Texto Transcrito", value=transcribed_text, height=200, disabled=True)
                st.success("Transcrição concluída! Você pode começar a conversar sobre o conteúdo abaixo.")
            else:
                st.error("Falha na transcrição do áudio.")
        else:
            st.error("Falha no download do áudio. Verifique a URL e tente novamente.")
    else:
        st.warning("Por favor, insira uma URL do YouTube.")

# --- Chat Interface ---
if st.session_state.transcription_text:
    st.markdown("---")
    st.header("Chat sobre o Conteúdo Transcrito")

    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if user_input := st.chat_input("Faça uma pergunta sobre a transcrição..."):
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                response = st.session_state.chain.invoke({
                    "contexto": st.session_state.transcription_text,
                    "pergunta": user_input
                })
                bot_response = response.content
                st.markdown(bot_response)
                st.session_state.chat_history.append({"role": "assistant", "content": bot_response})
else:
    st.info("Insira uma URL do YouTube e clique em 'Transcrever Áudio e Preparar Chat' para começar.")
