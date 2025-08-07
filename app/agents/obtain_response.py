from .agent import Agent

context_obtain_response = """
Responde solo "SI" o "NO" a la pregunta
"""


class ObtainResponseAgent(Agent):
    def __init__(self, context=context_obtain_response) -> None:
        super().__init__(context, max_tokens=50,temperature=0,top_p=0,presence_penalty=0,frequency_penalty=0)

    def receive_message(self, message_system: str, messages:list=[]) -> str:
        return super()._receive_message(message_user=message_system,messages=messages)

