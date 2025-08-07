from .agent import Agent

context_obtain_topic="""
¿Que sentencia legal concreta necesita el usuario?
Responde con el nombre en concreto de trámite judicial.
"""

class ObtainTopicAgent(Agent):
    def __init__(self, context=context_obtain_topic) -> None:
        super().__init__(context, max_tokens=50,temperature=0,top_p=0,presence_penalty=0,frequency_penalty=0)

    def receive_message(self, message_user: str, messages:list=[]) -> str:
        message_complete = f"Dime solo el nombre de la sentencia legal que ayudaría al usuario, mensaje del usuario: '{message_user}' si no está claro lee los demás mensajes y si aún así no sabes di 'NS'"
        response = super()._receive_message(message_user=message_complete,messages=messages)
        if "**" in response:
            list_response = response.split("**")
            if len(list_response) > 2:
                response = list_response[-2]
        return response

