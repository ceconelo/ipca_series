import sys
import time
from loguru import logger as log


def countdown(num_of_secs):
    while num_of_secs:
        mins, secs = divmod(num_of_secs, 60)
        timer = '\rTry again in: {:02d}:{:02d}'.format(mins, secs)
        sys.stdout.write(timer)
        sys.stdout.flush()
        time.sleep(1)
        num_of_secs -= 1
    sys.stdout.write('\n')



