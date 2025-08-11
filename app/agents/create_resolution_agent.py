from .agent import Agent

context_create_resolution="""
Tienes que crear la presentación de escritos y documentos legales ante el juzgado.
Usa solo los datos dados, nunca uses la palabra "null".
Antes de redactar, considera las directrices globales: ofrecer varias alternativas con ventajas e inconvenientes, seleccionar la recomendación más favorable y calcular una estimación económica máxima del litigio.
Redacta con precisión legal, pero de manera clara para que el cliente entienda el contenido.
Finaliza con una oferta de ayuda para implementar la recomendación.
"""

class CreateResolutionAgent(Agent):
    def __init__(self, context=context_create_resolution) -> None:
        super().__init__(context, max_tokens=1705)

    def receive_message(self, scheme: str, lawyer_data: str) -> str:
        message_complete = "Haz un documento legal para entregar al juzgado con los datos de este esquema: "+scheme+"; datos del abogado: "+lawyer_data
        return super()._receive_message(message_user=message_complete)
