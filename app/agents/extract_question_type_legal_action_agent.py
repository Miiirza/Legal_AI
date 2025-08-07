from .agent import Agent

context_extract_question_type_legal_action="""
Necesito una lista de datos que necesito preguntarle a mi cliente para saber que trámite legal le viene mejor en su caso.
NO pongas datos personales, solo los datos minimos y necesarios para ver cuál sería la mejor opción en este caso. Ordenalos de más a menos importante.
"""

class ExtractQuestionTypeLegalActionAgent(Agent):
    def __init__(self, context=context_extract_question_type_legal_action) -> None:
        super().__init__(context, max_tokens=2000, temperature=0,top_p=0,presence_penalty=0,frequency_penalty=0)

    def receive_message(self, message_user: str, topic:str, messages:list=[], boe:str="") -> str:
        message_complete = "Genera una lista de datos para especificar que hacer en el caso: "+topic+". Último mensaje del usuario:"+message_user
        if len(boe)>0:
            message_complete = message_complete+". Teniendo en cuenta: "+boe
        return super()._receive_message(message_user=message_complete, messages=messages)
