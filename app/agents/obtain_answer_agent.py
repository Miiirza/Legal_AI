from .agent import Agent

context_obtain_answer = """
Dado un dato con valor null, sustituye null por su verdadero valor.
Si no tienes suficiente información para cambiar el valor, devuelvelo como estaba anteriormente, poniendo null.
"""


class ObtainAnswerAgent(Agent):
    def __init__(self, context=context_obtain_answer) -> None:
        super().__init__(context, max_tokens=50,temperature=0,top_p=0,presence_penalty=0,frequency_penalty=0)

    def receive_message(self, message_user: str, data: str, messages:list=[]) -> str:
        return super()._receive_message(message_user=f"Dato a rellenar: '{data}' y último mensaje del usuario: '{message_user}'. Devuelve SOLO el dato a rellenar modificado.", messages=messages)
