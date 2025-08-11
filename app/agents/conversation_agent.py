from .agent import Agent

context_conversation = """
Eres un asistente legal que sigue estas directrices:
Busca en internet y en tu base de datos para encontrar las preguntas necesarias que harías como abogado.
Responde de forma clara sin frases introductorias innecesarias.
Haz solo una pregunta por mensaje.
Una vez que el usuario responda, interésate por el resultado óptimo que busca.
En base a sus respuestas, ofrécele varias alternativas (cada una con dos ventajas y dos inconvenientes), haz una recomendación de la opción con mejor potencial y concluye con una estimación económica máxima de un posible litigio.
Finalmente, ofrece ayuda para implementar tu recomendación.
Usa formato plano, sin HTML ni datos entre corchetes
"""


class ConversationAgent(Agent):
    def __init__(self, context=context_conversation) -> None:
        super().__init__(context, max_tokens=1705)

    def receive_message(self, message_user:str, messages:list=[], max_tokens=0) -> str:
        return super()._receive_message(message_user=message_user,messages=messages, max_tokens=max_tokens)

    def first_message(self):
        messages=[{'role': 'system', 'content': context_conversation}, {'role': 'system', 'content': 'Saluda al usuario de forma general'}]
        return super()._create_response(messages=messages)
