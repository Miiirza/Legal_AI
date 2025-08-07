import openai
import io
import logging
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()
API_KEY = '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'
#api keky openai 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
# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class AudioTranscriber:
    def __init__(self, model: str = "whisper-1"):
        if not API_KEY:
            logging.error("API_KEY no está definida en el entorno")
            raise ValueError("Falta API_KEY")
        
        self.client = openai.OpenAI(api_key=API_KEY)
        self.model = model
        logging.info(f"{self.__class__.__name__} inicializado con modelo {model}")

    def transcribe_audio(self, audio_bytes: bytes, filename: str = "audio.webm") -> str:
        try:
            logging.info(f"{self.__class__.__name__} comenzando transcripción de {filename}")
            audio_file = io.BytesIO(audio_bytes)
            audio_file.name = filename

            response = self.client.audio.transcriptions.create(
                model=self.model,
                file=audio_file
            )

            text = response.text
            logging.info(f"{self.__class__.__name__} transcripción completada")
            return text
        
        except Exception as e:
            logging.error(f"{self.__class__.__name__} error al transcribir audio: {str(e)}")
            raise RuntimeError(f"Error al transcribir audio: {str(e)}")

