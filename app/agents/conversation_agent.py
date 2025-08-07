from .agent import Agent

context_conversation = """
Eres un asistente legal para crear resoluciones legales, resuelve las dudas del cliente.
No tienes nombre. No pongas datos ente [].
Procura que la conversación sea ligera y natural.
Responde con el respeto y cuidado que la situación requiera.
Si haces preguntas haz solo UNA por mensaje.
Usa formato plano, NO HTML.
"""


class ConversationAgent(Agent):
    def __init__(self, context=context_conversation) -> None:
        super().__init__(context, max_tokens=1705)

    def receive_message(self, message_user:str, messages:list=[], max_tokens=0) -> str:
        return super()._receive_message(message_user=message_user,messages=messages, max_tokens=max_tokens)

    def first_message(self):
        messages=[{'role': 'system', 'content': context_conversation}, {'role': 'system', 'content': 'Saluda al usuario de forma general'}]
        return super()._create_response(messages=messages)
