from loguru import logger as log

from api.servicodados_ibge import CalendarioIPCA
from crontab import CronTab

'''
    This module is responsible for scheduling in crontab
'''


def set_schedules():
    reference = '2022-01-01'

    path_venv = None
    path_main = None

    if (path_venv is None) & (path_main is None):
        raise ValueError(f'Variables (path_venv / path_main) cannot be null')

    try:
        # Getting and iterating over calendar data
        for sched in CalendarioIPCA(reference).get_schedules():
            day = sched['date'].split('/')[0]
            month = sched['date'].split('/')[1]
            hour = sched['time'].split(':')[0]
            minutes = sched['time'].split(':')[1]

            user_cron = CronTab(user=True)
            # command = ~/path to virtual environment ~/path to the module to be executed by crontab
            job = user_cron.new(command=f'{path_venv} {path_main}')
            job.hour.on(hour)  # 10 hours
            job.day.on(int(day))
            job.minutes.on(int(minutes))
            job.month.on(int(month))

            user_cron.write()
        log.info('Scheduling done.')
    except BaseException as err:
        log.error('Error when trying to create schedules')
        log.error(err)


if __name__ == '__main__':
    set_schedules()
