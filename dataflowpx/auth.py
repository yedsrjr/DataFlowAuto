from datetime import datetime
import json, requests
from settings import Settings

def cnct_api_liberali(requisicao, api):
    url = f"{Settings().IP_API_LIBERALI}/{api}"
    headers = {
        'Authorization': Settings().AUTH_API_LIBERALI,
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=requisicao)
    print(f'Consultando tabelas - {datetime.now().replace(microsecond=0)}')
    retorno = response.json()
    
    return retorno, response

def busca_sap_api_query(q):
    query = json.dumps(q)
    response = cnct_api_liberali(query, "query")
    return response
