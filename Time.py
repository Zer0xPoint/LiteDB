import datetime
import time


def local_time():
    return time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())