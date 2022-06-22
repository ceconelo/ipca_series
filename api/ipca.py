import sidrapy
from loguru import logger as log


class Ipca:
    def __init__(self, start=None, end=None):
        if (start is None) | (end is None):
            raise ValueError('A start and end date is required')

        self.__start = start
        self.__end = end

    def get_series(self):
        log.info(f'Searching time series for the period: {self.__start} - {self.__end}')
        return sidrapy.get_table(
            table_code="1737",  # ipca
            territorial_level="1",
            ibge_territorial_code="all",  # all
            variable='63',
            period=f"{self.__start}-{self.__end}",
            verify_ssl=False
        )

    @staticmethod
    def last_update():
        return sidrapy.get_table(
            table_code="1737",  # ipca
            territorial_level="1",
            ibge_territorial_code="all",  # all
            variable='63',
            verify_ssl=False
        ).iloc[-1]['D3C'] # last line
