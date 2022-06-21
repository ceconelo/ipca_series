from loguru import logger as log

from api.servicodados_ibge import CalendarioIPCA


def main():
    today = datetime.today().strftime('%Y-%m-%d')
    ca = CalendarioIPCA(today)
    log.debug(ca.get_schedules())


if __name__ == '__main__':
    log.info('Starting...')
    main()
