from .agent import Agent, log_debug

context_question_scheme = """
Eres un asistente en temas legales, tienes que hablar con tacto al cliente.
Tu misión es recopilar los datos del cliente.
Manten una conversación amigable y con respeto al cliente, si te pregunta alguna duda respondele.
Evita repetir siempre el mismo inicio de frase.
Preguntale una unica cosa a la vez para no agobiar al cliente.
Intenta que las preguntas sean largas y que expliques exactamente que dato necesitas.
NO repitas los mensajes del usuario ni los datos del cliente.
"""


class CreateQuestionAgent(Agent):
    def __init__(self, context=context_question_scheme) -> None:
        super().__init__(context, max_tokens=1705, presence_penalty=0.6)

    def receive_message(self, message_user:str, next_topic: str, scheme: str, messages:list=[]) -> str:
        message_complete = f"Mensaje del usuario:'{message_user}', el siguiente dato que debes preguntarle es: '{next_topic}'."
        return super()._receive_message(message_user=message_complete,messages=messages)
