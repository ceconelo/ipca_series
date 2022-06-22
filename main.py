import os
import sys
import warnings
from datetime import datetime, timedelta

import pandas as pd
from loguru import logger as log

from api.ipca import Ipca
from utils import countdown

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


def get_last_month_update(saved_series):
    last_update = pd.to_datetime(saved_series.iloc[-1]['D2C'], format='%Y%m')
    log.info(f'Latest update: {last_update.strftime("%Y%m")}')
    return last_update


def main():
    display = total_attempts = 10

    while total_attempts != 0:
        saved_series = read_file(FILE)
        last_update = get_last_month_update(saved_series)

        available_data_on_site = Ipca.last_update()

        if available_data_on_site != last_update.strftime('%Y%m'):
            start = (last_update + timedelta(days=32)).strftime('%Y%m')  # add one mounth at the last date
            end = available_data_on_site

            ipca_series = Ipca(start=start, end=end).get_series()[1:]  # [1:] remove headers

            try:
                new_data = pd.concat([saved_series, ipca_series], ignore_index=True)
                new_data.to_csv(FILE, index=False)
                log.info('Updated file.')
                break
            except BaseException as err:
                log.error(f'An error occurred while trying to update the file: {FILE}')
                log.error(err)

        else:
            log.info('The file is already updated.')
            log.info(f'Attempts: {total_attempts}/{display}')
            countdown(60)
            total_attempts -= 1

        # ca = CalendarioIPCA(today)
        # log.debug(ca.get_schedules())


if __name__ == '__main__':
    log.info('Starting...')
    main()
