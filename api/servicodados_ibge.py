import requests
from http import HTTPStatus
from loguru import logger as log
from datetime import datetime

'''
    Consumindo API do ibge.
    Docs. https://servicodados.ibge.gov.br/api/docs
'''


class CalendarioIPCA:
    def __init__(self, date):
        self.__produto = '9256'  # ipca
        self.__query = f'?de={date}'
        self.__endpoint = f'https://servicodados.ibge.gov.br/api/v3/calendario/{self.__produto}{self.__query}'

    def get_schedules(self):
        result = requests.get(url=self.__endpoint)
        if result.status_code == HTTPStatus.OK:
            log.info(f'Request success: {self.__endpoint}')
            json_items = result.json().get('items')

            scheds = []
            for item in json_items:
                splited = item['data_divulgacao'].split(' ')
                scheds.append({
                    'date': splited[0],
                    'time': splited[1]
                })

            return scheds
        else:
            log.error('An error occurred while requesting the API.')
