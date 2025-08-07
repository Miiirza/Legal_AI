from .agent import Agent

context_create_resolution="""
Tienes que crear la presentación de escritos y documentos legales ante el juzgado.
Usa solo los datos dados, nunca uses la palabra "null".
"""

class CreateResolutionAgent(Agent):
    def __init__(self, context=context_create_resolution) -> None:
        super().__init__(context, max_tokens=1705)

    def receive_message(self, scheme: str, lawyer_data: str) -> str:
        message_complete = "Haz un documento legal para entregar al juzgado con los datos de este esquema: "+scheme+"; datos del abogado: "+lawyer_data
        return super()._receive_message(message_user=message_complete)
