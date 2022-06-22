from loguru import logger as log
from datetime import datetime, timedelta
import os, sys

import pandas as pd

from api.servicodados_ibge import CalendarioIPCA
from api.ipca import Ipca

import warnings

warnings.filterwarnings('ignore')

FILE = 'ipca_series.csv'


def read_file(file):
    log.info(f'Reading file: {file}')
    try:
        return pd.read_csv(file)
    except:
        log.warning('File not found')
        log.info('Creating a new time series file: Jan1995 - Jan2022')
        Ipca(start='199501', end='202201').get_series().to_csv(FILE, index=False)
        log.info(f'File created: {FILE}')
    finally:
        return pd.read_csv(file)


def get_last_mounth_update(saved_series):
    last_update = pd.to_datetime(saved_series.iloc[-1]['D2C'], format='%Y%m')
    log.info(f'Latest update: {last_update.strftime("%Y%m")}')
    return last_update


def main():
    saved_series = read_file(FILE)
    start = (get_last_mounth_update(saved_series) + timedelta(days=32)).strftime(
        '%Y%m')  # add one mounth at the last date
    end = datetime.today().strftime('%Y%m')  # current mounth

    if start == end:
        log.info('The file is already updated.')
        sys.exit(os.EX_OK)

    ipca_series = Ipca(start=start, end=end).get_series()[1:]  # [1:] remove headers

    try:
        new_data = pd.concat([saved_series, ipca_series], ignore_index=True)
        new_data.to_csv(FILE, index=False)
        log.info('Updated file.')
    except BaseException as err:
        log.error(f'An error occurred while trying to update the file: {FILE}')
        log.error(err)

    # ca = CalendarioIPCA(today)
    # log.debug(ca.get_schedules())


if __name__ == '__main__':
    log.info('Starting...')
    main()
    # Ipca(start='199501', end='202201').get_series().to_csv('ipca_series.csv', index=False)
