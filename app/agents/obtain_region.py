from .agent import Agent, log_warning
from fuzzywuzzy import process

context_obtain_region = """
Responde solo con el nombre de una provincia, tal cual como están en esta lista:
'Albacete'; 'Alicante'; 'Almería'; 'Araba/Álava'; 'Asturias'; 'Ávila'; 'Badajoz'; 'Balears, Illes'; 'Bizkaia'; 'Burgos'; 'Cáceres'; 'Cádiz'; 'Cantabria'; 'Castellón/Castelló'; 'Ciudad Real'; 'Córdoba'; 'Coruña, A'; 'Cuenca'; 'Gipuzkoa'; 'Girona'; 'Granada'; 'Guadalajara'; 'Huelva'; 'Huesca'; 'Jaén'; 'León'; 'Lleida'; 'Lugo'; 'Madrid'; 'Málaga'; 'Murcia'; 'Navarra'; 'Ourense'; 'Palencia'; 'Las Palmas'; 'Pontevedra'; 'La Rioja'; 'Salamanca'; 'Santa Cruz de Tenerife'; 'Segovia'; 'Sevilla'; 'Soria'; 'Tarragona'; 'Teruel'; 'Toledo'; 'Valencia/València'; 'Valladolid'; 'Zamora'; 'Zaragoza'; 'Ceuta'; 'Melilla'
"""

provinces = ['Albacete', 'Alicante', 'Almería', 'Araba/Álava', 'Asturias', 'Ávila', 'Badajoz', 'Balears, Illes', 'Bizkaia', 'Burgos', 'Cáceres', 'Cádiz', 'Cantabria', 'Castellón/Castelló', 'Ciudad Real', 'Córdoba', 'Coruña, A', 'Cuenca', 'Gipuzkoa', 'Girona', 'Granada', 'Guadalajara', 'Huelva', 'Huesca', 'Jaén', 'León', 'Lleida', 'Lugo', 'Madrid', 'Málaga', 'Murcia', 'Navarra', 'Ourense', 'Palencia', 'Las Palmas', 'Pontevedra', 'La Rioja', 'Salamanca', 'Santa Cruz de Tenerife', 'Segovia', 'Sevilla', 'Soria', 'Tarragona', 'Teruel', 'Toledo', 'Valencia/València', 'Valladolid', 'Zamora', 'Zaragoza', 'Ceuta', 'Melilla']

class ObtainRegionAgent(Agent):
    def __init__(self, context=context_obtain_region) -> None:
        super().__init__(context, max_tokens=10,temperature=0,top_p=0,presence_penalty=0,frequency_penalty=0)

    def receive_message(self, message_system: str, messages:list=[]) -> str:
        province = super()._receive_message(message_user=message_system,messages=messages)
        true_region, score = process.extractOne(province, provinces)
        while province not in provinces or score < 70:
            log_warning('Province not found correctly')
            province = super()._receive_message(message_user="Dame SOLO el nombre de la provincia de la que debería coger el abogado. Las provincias posibles son: "+",".join(provinces),messages=messages)
            true_region, score = process.extractOne(province, provinces)
        return true_region


