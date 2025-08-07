from .agent import Agent

context_extract_data_need="""
Eres un asistente experto en derecho, di todos los datos que necesitarias para que un abogado haga un escrito a un juez sobre el tema que se te pase.
Solo los datos que necesita el abogado para hacer el escrito o demanda, no los que necesita el juez.
No añadas los datos de los abogados/procuradores ni de las firmas.
"""

class ExtractDataNeedAgent(Agent):
    def __init__(self, context=context_extract_data_need) -> None:
        super().__init__(context, max_tokens=2000, temperature=0,top_p=0,presence_penalty=0,frequency_penalty=0)

    def receive_message(self, message_user: str, topic:str,messages:list=[], boe:str="") -> str:
        message_complete = "Genera una demanda judicial para el caso de "+topic+". Debe incluir solo los datos del demandante y la descripción del conflicto. No incluyas información sobre el abogado del demandado, salvo que se trate de un caso de mutuo acuerdo y se especifique. Esto se hace porque el usuario ha dicho:"+message_user
        if len(boe)>0:
            message_complete = message_complete+". Teniendo en cuenta: "+boe
        return super()._receive_message(message_user=message_complete,messages=messages)
