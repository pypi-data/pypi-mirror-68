import time
from datetime import datetime, timedelta

class DateUtils:
    '''
    Ref: https://stackoverflow.com/questions/7479777/difference-between-python-datetime-vs-time-modules

    '''
    def __init__(self):
        pass


    @staticmethod
    def get_unix_timestamp(): # type: () -> int
        ''' Same as datetime.utcnow().timestamp() 13 digits'''
        return int(time.time() * 1000)

    @staticmethod
    def get_unix_time_diff(seconds=0): # type: (int) -> int
        return DateUtils.get_unix_timestamp() - seconds * 1000

    @staticmethod
    def convert_unix_datetime(unix_time): # type: (int) -> datetime
        return datetime.utcfromtimestamp(unix_time)

    @staticmethod
    def get_mysql_datetime(): # type: () -> str
        return time.strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def now():
        return datetime.now()

    @staticmethod
    def datetime_second_diff(seconds=0):
        return datetime.now() - timedelta(seconds=seconds)

    @staticmethod
    def get_current_time_str():
        return str(datetime.now())[11:19]

if __name__ == '__main__':
    d = DateUtils()

    # print(d.get_unix_timestamp())
    # print(type(DateUtils.convert_unix_datetime(1588264584)))
    print(type(DateUtils.get_mysql_datetime()))

    # print(datetime(2009, 5, 5))