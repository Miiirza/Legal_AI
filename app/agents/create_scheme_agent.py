from .agent import Agent

context_create_scheme="""
Eres un asistente experto en derecho que genera esquemas estructurados.
No hagas una sección con varios valores, un dato por cada valor.
Responde con un esquema en el siguiente formato: 'ESQUEMA; dato1: null; dato2: null; dato3: null', utilizando los datos que se deben solicitar a un cliente para realizar una resolución jurídica.
Pon siempre en los valores null.
"""

class CreateSchemeAgent(Agent):
    def __init__(self, context=context_create_scheme) -> None:
        super().__init__(context,max_tokens=1705, temperature=0, top_p=0, presence_penalty=0, frequency_penalty=0)

    def receive_message(self, summary: str) -> str:
        message_complete = "Hazme un esquema con TODOS los datos en: "+summary
        return super()._receive_message(message_user=message_complete)
