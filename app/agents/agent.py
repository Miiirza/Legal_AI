import os
import requests
from dotenv import load_dotenv
import json
import logging

load_dotenv()
API_KEY = os.getenv("API_KEY")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def log_debug(message:str) -> None:
    logging.debug(message)

def log_info(message:str) -> None:
    logging.info(message)

def log_warning(message:str) -> None:
    logging.warning(message)

def log_error(message:str) -> None:
    logging.error(message)

def log_critical(message:str) -> None:
    logging.critical(message)


if not API_KEY or len(API_KEY) == 0:
    log_error("API_KEY environment variable is not set")
else:
    log_info("API_KEY environment variable is set")


class Agent:
    def __init__(self, context: str = "Busca en internet y en tu base de datos y encuentra las preguntas necesarias que tendrías que hacer, como si fueras un abogado, para entender y ayudar a solucionar las casuísticas que te presentan distintos usuarios. Una vez que éstos respondan a tus preguntas, interésate por el resultado óptimo que buscan y, en base a sus respuestas, ofréceles varias alternativas con dos ventajas e inconvenientes en cada una de las alternativas. A continuación, haz la recomendación que mejor resultado potencial pueda ofrecer a los usuarios de acuerdo con el resultado óptimo que buscan. Finalmente concluye con una estimación económica, siempre pensando en máximos, de cual podría ser el resultado de un posible litigio si los clientes siguen tus recomendaciones. Acaba ofreciendo ayuda para implementar la tarea que recomiendas", model:str='anthropic/claude-sonnet-4',
                 max_tokens:int=9000, temperature:float=0.6, top_p:float=0.6, presence_penalty:float=0.6, frequency_penalty:float=0.4) -> None:
        log_info(f"{self.__class__.__name__} created")
        self.context = context
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.presence_penalty = presence_penalty
        self.frequency_penalty = frequency_penalty
        self.model = model

    def _receive_message(self, message_user:str, messages:list=[], max_tokens=0) -> str:
        if max_tokens == 0:
            max_tokens = self.max_tokens

        if len(messages)>1:
            messages = messages.copy()
            messages[0]['content'] = self.context
            messages.append({'role': 'user', 'content': message_user})
            log_debug(f"{self.__class__.__name__} Using history of messages")

        else:
            messages = [{'role': 'system', 'content': self.context}, {'role': 'user', 'content': message_user}]
            log_debug(f"{self.__class__.__name__} Not using history of messages")

        reply = self._create_response(messages=messages, max_tokens=max_tokens)

        return reply

    def _create_response(self, messages: list, max_tokens=0) -> str:
        if max_tokens == 0:
            max_tokens = self.max_tokens
        log_info(f"{self.__class__.__name__} requesting response")
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={
                "model": self.model,
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": self.temperature,
                "top_p": self.top_p,
                "presence_penalty": self.presence_penalty,
                "frequency_penalty": self.frequency_penalty
            },
        ).json()

        if "choices" in response and len(response["choices"]) > 0:
            reply = response["choices"][0]["message"]["content"]
            return str(reply)
        else:
            log_error(f"{self.__class__.__name__} API couldn't generate a response: " + json.dumps(response))
            return "Lo siento, no pude generar una respuesta."
