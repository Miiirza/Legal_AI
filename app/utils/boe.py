import requests
from fuzzywuzzy import process

headers = {
    "Accept": "application/xml"
}

url = "https://boe.es/datosabiertos/api/legislacion-consolidada/id/"

boe_articles={
        "divorcio":["BOE-A-1981-16216","BOE-A-2005-11864"],
        "desalojo":["BOE-A-2018-7579","BOE-A-2018-17293","BOE-A-2020-11243"],
        "concurso de acreedores": ["BOE-A-2015-2109"],
        "segunda oportunidad":["BOE-A-2015-2109"]
}

def obtain_boe(topic:str) -> str:
    result = ""
    true_topic, score = process.extractOne(topic, boe_articles.keys())
    if score > 70:
         for boe in boe_articles[true_topic]:
            response = requests.get(url+boe, headers=headers)
            if response.status_code == 200:
                text=response.text
                result += text+ 5*"\n"
    return result
