from .agent import Agent, log_debug

context_edit_scheme = """
Ayudame a completar un esquema leyendo los mensajes de chat que manda el cliente.
Guardas las fechas con el formato: Día del nombre del mes de año. Y los correos electronicos guarda tambien el dominio (nombreuser@dominio).
Pero si hay algún dato que no existe pon que no existe, 0 o el motivo por el que no se tiene dicho dato. 
El valor null es solo si aún no se ha dado esa información, si la información no es necesario pon de valor que no se necesita saber.
Si un dato no existe debido al valor de otro dato, pon que no existe.
Si lo ves necesario crea nuevos datos.
Usa esta estructura: "SCHEMME; data1: null; data2: null; data3: null" devolviendo el mensaje igual a como te lo mandan cambiando unicamente los valores.
"""


class EditSchemeAgent(Agent):
    def __init__(self, context=context_edit_scheme) -> None:
        super().__init__(context, max_tokens=2000, temperature=0,top_p=0,presence_penalty=0,frequency_penalty=0)


    def receive_message(self, message_user:str, scheme: str, messages:list=[]) -> str:
        message_complete = f"Mensaje del cliente:{message_user} y el esquema '{scheme}'"
        return super()._receive_message(message_user=message_complete,messages=messages)
