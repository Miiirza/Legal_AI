from .agent import Agent, log_debug

context_question_scheme = """
Eres un asistente legal, cuya misión es recopilar toda la información necesaria para la situación legal del cliente siguiendo estas directrices:
Busca en internet y en tu base de datos para determinar qué preguntas harías como abogado en esta casuística.
Responde de forma clara sin frases introductorias innecesarias.
Haz solo una pregunta por mensaje y evita repetir siempre el mismo inicio de frase.
Si el cliente te hace una pregunta, respóndele sin desviarte de tu objetivo de recopilar datos.
Evita repetir datos ya proporcionados y no reproduzcas textualmente los mensajes del usuario.
"""


class CreateQuestionAgent(Agent):
    def __init__(self, context=context_question_scheme) -> None:
        super().__init__(context, max_tokens=1705, presence_penalty=0.6)

    def receive_message(self, message_user:str, next_topic: str, scheme: str, messages:list=[]) -> str:
        message_complete = f"Mensaje del usuario:'{message_user}', el siguiente dato que debes preguntarle es: '{next_topic}'."
        return super()._receive_message(message_user=message_complete,messages=messages)
