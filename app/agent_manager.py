from agents.agent import log_info, log_warning, log_error, Agent
from agents.create_scheme_agent import CreateSchemeAgent
from agents.create_question_agent import CreateQuestionAgent
from agents.obtain_topic_agent import ObtainTopicAgent
from agents.create_resolution_agent import CreateResolutionAgent
from agents.conversation_agent import ConversationAgent
from agents.edit_scheme_agent import EditSchemeAgent
from agents.extract_data_need_agent import ExtractDataNeedAgent
from agents.obtain_response import ObtainResponseAgent
from agents.obtain_region import ObtainRegionAgent
from agents.obtain_answer_agent import ObtainAnswerAgent
from agents.extract_question_type_legal_action_agent import ExtractQuestionTypeLegalActionAgent
from agents.validate_document_agent import ValidateDocumentAgent
from utils.patterns import extract_pattern_schemme, extract_pattern_list_values, delete_headers
from utils.boe import obtain_boe
from lawyers import obtain_lawyer

class AgentManager:
    def __init__(self):
    
        self.in_document_validation_mode=False
        self.last_document_text=''
        self.last_analysis=''
    
        self.phase=0
        self.scheme=""
        self.dictScheme = {"Done":[], "Null":[]}
        self.messages = [{'role': 'system', 'content': 'context'}]
        # Agents
        self.conversation_agent = ConversationAgent()
        self.create_scheme_agent = CreateSchemeAgent()
        self.create_question_agent = CreateQuestionAgent()
        self.create_resolution_agent = CreateResolutionAgent()
        self.edit_scheme_agent = EditSchemeAgent()
        self.extract_data_need_agent = ExtractDataNeedAgent()
        self.extract_question_type_legal_action_agent = ExtractQuestionTypeLegalActionAgent()
        self.obtain_topic_agent = ObtainTopicAgent()
        self.obtain_response_agent = ObtainResponseAgent()
        self.obtain_region_agent = ObtainRegionAgent()
        self.obtain_answer_agent = ObtainAnswerAgent()
        self.validate_document_agent=ValidateDocumentAgent() #variable que añadi
        
        
    def looks_like_document(self, text: str) -> bool:
        if len(text.split()) > 300:
            return True
        if any(word in text.lower() for word in ["ley", "artículo", "disposición", "boe", "resolución", "sentencia"]):
            return True
        return False


    def receive_message(self, message_user: str) -> str:
        '''
        if self.in_document_validation_mode:
            if not self.is_document_question(message_user):
                self.in_document_validation_mode=False
                self.last_document_text=''
                self.last_analysis=''
            return self.phase_document_QA(message_user)
        '''
        if self.looks_like_document(message_user):
            analysis = self.validate_document_agent.receive_message(message_user)
            self.last_analysis = analysis
            self.last_document_text = message_user


            # Guardamos análisis como parte de la conversación
            self.messages.append({'role': 'assistant', 'content': f"(Análisis del documento subido)\n{analysis}"})


            # Reescribimos el mensaje del usuario para integrarlo
            message_user = f"He subido un documento, aquí está su análisis: {analysis}"


        message_bot = ""

        if self.phase == 0:
            #We do not know the topic, we only chat with the user
            message_bot = self.phase_conversation(message_user)

        elif self.phase == 1:
            #We know the topic, we see if the user wants to start the solution
            message_bot = self.phase_start_or_not(message_user)

        elif self.phase == 2:
            #We obtain data of the user to see the better solution
            message_bot = self.phase_questions(message_user)

        elif self.phase == 3:
            #To know exactly what the user wants
            message_bot = self.phase_select_resolution_type(message_user)

        elif self.phase == 4:
            #Check if user wants that topic
            message_bot = self.phase_start_or_not_total_topic(message_user)

        elif self.phase == 5:
            #We know the topic and have the scheme, we start doing the questions to complete
            message_bot = self.phase_questions(message_user)

        elif self.phase == 6:
            #Talk with the user to know if they want a lawyer
            message_bot = self.phase_lawyer_data(message_user)

        elif self.phase == 7:
            #We have all the answers, talk with the user to know if they want to create a resolution
            message_bot = self.phase_create_resolution_or_not(message_user)

        elif self.phase == 8:
            #The user don't want a resolution, but maybe a summary of the lawyer
            message_bot = self.phase_create_summary_or_not(message_user)

        elif self.phase == 9:
            message_bot = self.conversation_agent.receive_message(message_user=message_user,messages=self.messages)

        else:
            message_bot = "Error inesperado"

        self.messages.append({'role': 'user', 'content': message_user})
        self.messages.append({'role': 'system', 'content': message_bot})
        return message_bot
    
    def is_document_question(self, user_input:str) -> bool:
        if not self.last_analysis:
            return False
        check_prompt=f''' El usuatio a preguntado esto: "{user_input}"
        Este es el análisis de un documento legal que hiciste previamente: {self.last_analysis}
        ¿La pregunta del usuario se refiere a ese documento o a su análisis? Responde solo con "Sí" o "No"'''
        answer= self.conversation_agent.receive_message(message_user=check_prompt, messages=[])
        return 'sí' in answer.lower()
    
    def validate_document(self, message_user: str) ->str: #funcion que añadí
        return self.validate_document_agent.receive_message(message_user) #causa problemas

    def get_scheme(self) -> dict:
        return self.dictScheme

    def get_summary(self) -> str:
        return self.conversation_agent.receive_message(
            message_user="Creame un resumen para presentarselo a un abogado de lo hablado hasta ahora. No añadas datos que aún no se tengan. Y pásame solo el resumen.",
            messages=self.messages,
            max_tokens=1705) #antes 2000

    def first_message(self):
        message_bot = self.conversation_agent.first_message()
        self.messages.append({'role': 'system', 'content': message_bot})
        return message_bot
        
    def phase_document_QA(self, message_user:str) -> str:  #integrado digamos en paralelo para validar documentos
        if not self.last_analysis:
            self.last_analysis= self.validate_document_agent.receive_message(
                document_text=self.last_document_text,
                messages=self.messages
            )
            self.messages.append({'role':'assistant', 'content': self.last_analysis})
        full_prompt=f'''Este es el análisis de un documento legl que hiciste antes: {self.last_analysis}
        El usuario pregunta: {message_user}. Responde basándote solo en ese análisis y el contenido del documento.'''
        
        response=self.conversation_agent.receive_message(message_user=full_prompt, messages=self.messages)
        
        self.messages.append({'role':'assistant', 'content':response})
        return response

    def phase_conversation(self, message_user:str) -> str:
        topic = self.obtain_topic_agent.receive_message(message_user=message_user, messages=self.messages)
        if topic == 'NO' or topic == 'NS':
            message_bot = self.conversation_agent.receive_message(message_user=message_user, messages=self.messages)
        else:
            # We detect the topic and ask if they want a resolution
            self.phase = 1
            self.topic = topic
            message_bot = self.conversation_agent.receive_message(
                message_user="Preguntale al cliente si le podemos hacer una preguntas para ayudarle legalmente para el tema'" + topic + "', el ultimo mensaje del usuario es:" + message_user,
                messages=self.messages)
        return message_bot

    def phase_start_or_not(self, message_user:str) -> str:
        if 'NO' == self.obtain_response_agent.receive_message(
                message_system="¿El usuario quiere que le ayudemos en ese tema legal? Mensaje del usuario: " + message_user,
                messages=self.messages):
            self.phase = 0
            message_bot = self.phase_conversation(message_user)
        else:
            self.phase = 2
            boe = obtain_boe(self.topic)
            summary = self.extract_question_type_legal_action_agent.receive_message(topic=self.topic, message_user=message_user, messages=self.messages, boe=boe)
            scheme = self.create_scheme_agent.receive_message(summary=summary)
            scheme_dict = extract_pattern_list_values(scheme)
            while scheme_dict["Null"] is None or len(scheme_dict["Null"]) == 0:
                log_warning("Scheme incorrect, recreating...")
                scheme = self.create_scheme_agent.receive_message(
                    summary="Haz el esquema con el formato correcto. Resumen: " + summary)
                scheme_dict = extract_pattern_list_values(scheme)
            self.scheme = scheme
            self.dictScheme = scheme_dict
            message_bot = self.phase_questions(message_user)


        return message_bot



    def phase_select_resolution_type(self, message_user:str) -> str:
        if 'NO' == self.obtain_response_agent.receive_message(
                message_system="¿El usuario ha elegido exactamente que quiere hacer? Mensaje del usuario: " + message_user,
                messages=self.messages):
            message_bot = self.conversation_agent.receive_message(message_user=message_user, messages=self.messages)
        else:
            topic = self.obtain_topic_agent.receive_message(message_user=message_user, messages=self.messages)
            if topic == 'NS':
                message_bot = self.conversation_agent.receive_message(message_user=message_user, messages=self.messages)
            else:
                self.topic = topic
                self.phase = 4
                message_bot = self.conversation_agent.receive_message(message_user="Preguntale si quiere empezar el proceso judicial de:"+self.topic, messages=self.messages)

        return message_bot

    def phase_start_or_not_total_topic(self, message_user:str) -> str:
        if 'NO' == self.obtain_response_agent.receive_message(
                message_system="¿El usuario quiere comenzar el procedimiento legal? Mensaje del usuario: " + message_user,
                messages=self.messages):
            self.phase = 3
            message_bot = self.phase_select_resolution_type(message_user)
        else:
            self.phase = 5
            boe = obtain_boe(self.topic)
            summary = self.extract_data_need_agent.receive_message(topic=self.topic, message_user=message_user, boe=boe)
            scheme = self.create_scheme_agent.receive_message(summary=summary)
            scheme_dict = extract_pattern_list_values(scheme)
            while scheme_dict["Null"] is None or len(scheme_dict["Null"]) == 0:
                log_warning("Scheme incorrect, recreating...")
                scheme = self.create_scheme_agent.receive_message(
                    summary="Haz el esquema con el formato correcto. Resumen: " + summary)
                scheme_dict = extract_pattern_list_values(scheme)
            self.scheme = scheme
            self.dictScheme = scheme_dict
            message_bot = self.phase_questions(message_user)

        return message_bot



    def phase_questions(self, message_user:str) -> str:
        scheme_edit = self.edit_scheme_agent.receive_message(message_user=message_user, scheme=self.scheme, messages=self.messages)
        scheme_edit_dict = extract_pattern_list_values(scheme_edit)
        len_edit=len(scheme_edit_dict["Null"])+len(scheme_edit_dict["Done"])
        len_actual=len(self.dictScheme["Null"])+len(self.dictScheme["Done"])
        while len_edit == 0 or len_edit+5 < len_actual:
            log_warning("Scheme incorrect, recreating...")
            scheme_edit = self.edit_scheme_agent.receive_message(message_user="Usa la estructura de esquema correcto, no elimines datos."+message_user, scheme=self.scheme, messages=self.messages)
            len_edit = len(scheme_edit_dict["Null"]) + len(scheme_edit_dict["Done"])
        self.scheme = scheme_edit
        self.dictScheme = scheme_edit_dict
        if len(scheme_edit_dict["Null"]) == 0:
                if self.phase == 2:
                    self.phase = 3
                    message_bot = self.explainOptions(message_user)
                if self.phase == 5:
                    self.phase = 6
                    message_bot = self.conversation_agent.receive_message(
                            message_user="Informale al cliente de que necesitara un abogado para entregar la resolucion, que nosotros podemos darle uno o en casa de tener un abogado nos puede dar los datos de su abogado.",
                            messages=self.messages)
        else:
            firstNull = self.dictScheme['Null'][0]
            nulls = self.dictScheme['Null']
            dones = self.dictScheme['Done']
            response = self.obtain_answer_agent.receive_message(message_user=message_user, data=firstNull, messages=self.messages)

            while firstNull and ('null' not in str(response) and '[' not in str(response)):
                nulls.pop(0)
                dones.append(response)
                self.scheme = self.scheme.replace(firstNull, dones[-1])
                self.dictScheme = {"Null": nulls, "Done": dones}
                if self.dictScheme['Null'] is not None and len(self.dictScheme['Null'])>0:
                    firstNull = self.dictScheme['Null'][0]
                    response = self.obtain_answer_agent.receive_message(message_user=message_user,
                                                                        data=firstNull,
                                                                        messages=self.messages)
                else:
                    firstNull = None
                    break

            if firstNull is not None:
                message_bot = self.create_question_agent.receive_message(message_user=message_user, next_topic=firstNull,
                                                                     scheme=self.scheme, messages=self.messages)
                message_bot = delete_headers(message_bot)
            else:
                message_bot = 'FIN'

            if 'FIN' in message_bot.upper():
                if self.phase == 2:
                    self.phase = 3
                    message_bot = self.explainOptions(message_user)
                if self.phase == 5:
                    self.phase = 6
                    message_bot = self.conversation_agent.receive_message(
                            message_user="Informale al cliente de que necesitara un abogado para entregar la resolucion, que nosotros podemos darle uno o en casa de tener un abogado nos puede dar los datos de su abogado.",
                            messages=self.messages)
        return message_bot

    def explainOptions(self, message_user):
        message_bot = self.conversation_agent.receive_message(message_user="Dile las distintas formas de abordar el problema al usuario y dale otras variaciones, con sus ventajas y desventajas especificas en su caso. El ultimo mensaje del usuario es: '"+message_user+"' y el problema a resolver es:"+self.topic, messages=self.messages, max_tokens=1705) #antes 2000
        return message_bot

    def phase_create_resolution_or_not(self, message_user:str) -> str:
        if 'NO' != self.obtain_response_agent.receive_message(
                message_system="¿El usuario quiere que se le haga una resolución? Mensaje del usuario: " + message_user,
                messages=self.messages):
            self.phase = 9
            message_bot = self.createResoluion()
        else:
            self.phase = 8
            message_bot = self.conversation_agent.receive_message(message_user="Preguntale si quiere que se haga un resumen para pasarselo al abogado.", messages=self.messages)
        return message_bot

    def phase_create_summary_or_not(self, message_user:str) -> str:
        if 'NO' != self.obtain_response_agent.receive_message(
                message_system="¿El usuario quiere que se le haga un resumen? Mensaje del usuario: " + message_user,
                messages=self.messages):
            self.phase = 9
            message_bot = self.conversation_agent.receive_message(
                message_user="Creame un resumen para presentarselo a un abogado de lo hablado hasta ahora.",
                messages=self.messages,
                max_tokens=1705) #antes 2000
        else:
            self.phase = 9
            message_bot = self.conversation_agent.receive_message(message_user=message_user, messages=self.messages)
        return message_bot


    def question_what_todo(self):
        self.phase = 7
        return self.conversation_agent.receive_message(
                message_user="Ya tenemos todos los datos del cliente, preguntale al cliente si quiere que le hagamos una resolucion juridica.",
                messages=self.messages)

    def phase_lawyer_data(self, message_user:str) -> str:
        if 'NO' != self.obtain_response_agent.receive_message(
                message_system="¿El cliente quiere que le ofrezcamos uno de nuestros abogados? Mensaje del usuario: " + message_user,
                messages=self.messages):
            # We give the use one of our lawyers
            region = self.obtain_region_agent.receive_message(
                message_system="Nombre de la provincia de la que debería coger el abogado.", messages=self.messages)
            self.lawyer_data = obtain_lawyer(region)
            message_bot = self.question_what_todo()
        elif 'NO' != self.obtain_response_agent.receive_message(
                message_system="¿Ha dado datos de su abogado? Mensaje del usuario: " + message_user,
                messages=self.messages):
            # We do the resolution with the data of the lawyer of the client
            self.lawyer_data = self.conversation_agent.receive_message(
                message_user="Dime los datos del abogado del usuario. Mensaje del usuario: " + message_user,
                messages=self.messages)
            message_bot =self.question_what_todo()
        else:
            message_bot = self.conversation_agent.receive_message(
                message_user="Insistele en que necesitamos los datos de un abogado para hacer la resolucion y recuerdale que nosotros podemos darle un abogado. Mensaje del cliente:" + message_user,
                messages=self.messages)
        return message_bot

    def createResoluion(self) -> str:
        data = None
        if self.lawyer_data is None:
            data = obtain_lawyer("Madrid")
        else:
            data = self.lawyer_data
        resolution = self.create_resolution_agent.receive_message(scheme=self.scheme.replace("null", ""), lawyer_data=data)
        return resolution
