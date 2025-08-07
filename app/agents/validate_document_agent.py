from .agent import Agent

context_validate_document=''' 
Eres un agente legal que analiza documentos jurídicos. Tu tarea es determinar si el contenido de un documento legal es válido o contiene errores, omisiones o inconsistencias. 
Analiza la estructura, los datos obligatorios y la coherencia general del documento además de explicar el documento y sus partes.'''


class ValidateDocumentAgent(Agent):
    def __init__(self, context=context_validate_document) -> None:
        print('ValidateDocumentAgent inicializado')
        super().__init__(context, max_tokens=9000, temperature=0.3, top_p=1, presence_penalty=0, frequency_penalty=0) #comprobar todos estos atributos que no se que hacen

    def receive_message(self, document_text: str, messages:list=[]) -> str:
        response=super()._receive_message(message_user=document_text, messages=messages)
        return response
