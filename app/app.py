import streamlit as st
from agent_manager import AgentManager
from PyPDF2 import PdfReader
import docx
from streamlit_mic_recorder import mic_recorder
import io
import os
import tempfile
import wave
import json
from vosk import Model, KaldiRecognizer
#import pyttsx3
#import time

# Cargar modelo Vosk (solo una vez)
if "vosk_model" not in st.session_state:
    st.session_state.vosk_model = Model("vosk-model-small-es-0.42")

model = st.session_state.vosk_model

# INITIAL VALUES
if "agent" not in st.session_state:
    st.session_state.agent = AgentManager()
agent = st.session_state.agent
st.set_page_config(page_title="Legal AI", page_icon="⚖️")

# HEADER
col1, col2 = st.columns([5, 1])
col1.title("Legal AI")
beta_version = "0.6"
col1.markdown(f'<span style="background-color: gray; color: white; padding: 2px 6px; border-radius: 4px;">Beta v{beta_version}</span>', unsafe_allow_html=True)
col1.markdown(f'<p style="font-size: 10px;">Cambios en la nueva versión: obtener información del boe en ciertos casos.</p>', unsafe_allow_html=True)

st.markdown('Verificador de documentos legales')
uploaded_file = st.file_uploader('Sube un archivo legal (PDF o docx)', type=['pdf', 'docx'])

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

if uploaded_file is not None:
    if uploaded_file.name.endswith('.pdf'):
        file_text = extract_text_from_pdf(uploaded_file)
    elif uploaded_file.name.endswith('.docx'):
        file_text = extract_text_from_docx(uploaded_file)
    else:
        file_text = None
        st.error('Formato no compatible.')
    if file_text:
        st.success('Archivo subido y procesado correctamente')
        with st.expander('ver texto extraído'):
            st.text(file_text[:1500])
        if st.button("Validar documento"):
            agent.in_document_validation_mode = True
            agent.last_document_text = file_text
            response = agent.receive_message(file_text)
            st.session_state.messages.append({'role': 'assistant', 'content': response})
            #st.session_state.messages=st.session_state.messages[-20:]

if 'voice_input_text' not in st.session_state:
    st.session_state.voice_input_text = 0

if "messages" not in st.session_state:
    st.session_state.messages = []
    bot_response = agent.first_message()
    st.session_state.messages.append({"role": "assistant", "content": bot_response})

# --- AUDIO ---
audio = mic_recorder(
    start_prompt='🎙️ Grabar mensaje de voz',
    stop_prompt='Detener grabación',
    key='voice_input',
    just_once=False
)

# Mostrar historial de chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Mostrar historial de chat con opción "Leer más" para mensajes del bot
#for i, message in enumerate(st.session_state.messages):
#    with st.chat_message(message["role"]):
#        if message["role"] == "assistant":
#            texto = message["content"]
#            pos_interrogacion = texto.find("?")
#            if pos_interrogacion == -1:
#                st.write(texto)
#            else:
#                key_expandido = f"expandido_{i}"
#                if key_expandido not in st.session_state:
#                    st.session_state[key_expandido] = False
#
#                if st.session_state[key_expandido]:
#                    st.write(texto)
#                    if st.button("Leer menos", key=f"menos_{i}"):
#                        st.session_state[key_expandido] = False
#                else:
#                    st.write(texto[:pos_interrogacion + 1] + " ...")
#                    if st.button("Leer más", key=f"mas_{i}"):
#                        st.session_state[key_expandido] = True
#        else:
#            st.write(message["content"])




#def speak(text):
#    engine=pyttsx3.init()
    # Seleccionar español (España)
#    voices = engine.getProperty('voices')
#    engine.setProperty('voice', voices[26].id)
#    engine.say(text)
#    engine.runAndWait()
#    time.sleep(0.1)
#    engine.stop()

user_input = None
voice_text=''
if audio and "bytes" in audio:
    raw_bytes = audio["bytes"]
    with st.spinner("Transcribiendo audio con Vosk..."):
        try:
            with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as tmp_input:
                tmp_input.write(raw_bytes)
                tmp_input.flush()

            wav_path = tmp_input.name.replace(".webm", ".wav")
            # Convertir de webm a wav
            os.system(f"ffmpeg -i {tmp_input.name} -ar 16000 -ac 1 -f wav {wav_path} -loglevel quiet")

            wf = wave.open(wav_path, "rb")
            rec = KaldiRecognizer(model, wf.getframerate())

            results = []
            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                if rec.AcceptWaveform(data):
                    results.append(json.loads(rec.Result()))
            final_result = json.loads(rec.FinalResult())
            results.append(final_result)

            voice_text = " ".join([r.get("text", "") for r in results]).strip()
            #st.write(voice_text)

            if voice_text:
                # Muestra como mensaje del usuario
                with st.chat_message("user"):
                    st.write(voice_text)
                st.session_state.messages.append({"role": "user", "content": voice_text})

                # Llama al agente
                bot_response = agent.receive_message(voice_text)
                st.session_state.messages.append({"role": "assistant", "content": bot_response})
                #st.session_state.messages = st.session_state.messages[-20:]

                with st.chat_message("assistant"):
                    st.write(bot_response)
                #speak(bot_response) en render comentar esta linea

        except Exception as e:
            st.error(f"Error al transcribir: {e}")
            
    #st.experimental_rerun()
# Siempre mostrar campo de texto
user_input = st.chat_input("Escribe tu mensaje aquí...")
# Procesar entrada del usuario
if user_input:
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    bot_response = agent.receive_message(user_input)
    st.session_state.messages.append({"role": "assistant", "content": bot_response})

    with st.chat_message("assistant"):
        st.write(bot_response)
    #st.session_state.messages = st.session_state.messages[-20:]

# Funciones extra (Resumen, Esquema)
with col2:
    with st.popover("✉️"):
        if st.button("Resumen situación"):
            st.write(st.session_state.agent.get_summary())
        if st.button("Esquema proceso judicial"):
            scheme = st.session_state.agent.get_scheme()
            for i in scheme["Done"]:
                st.write(i)
            for i in scheme["Null"]:
                st.write(i.replace("null", "___"))


