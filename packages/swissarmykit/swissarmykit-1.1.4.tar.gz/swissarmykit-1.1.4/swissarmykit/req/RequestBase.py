import os
import abc

from swissarmykit.db.redisconnect import RedisConnect
from swissarmykit.utils.timer import Timer

try: from definitions_prod import *
except Exception as e: pass # Surpass error. Note: Create definitions_prod.py
from swissarmykit.utils.loggerutils import LoggerUtils
from cfscrape import CloudflareScraper


class RequestBase(abc.ABC):
    """
    Ref: https://github.com/uhub/awesome-python
    All method here for bridge between Base Component.
    """
    MAX_THREAD = 20
    redis: RedisConnect

    def __init__(self):
        self.is_log = False
        self.is_debug = False
        self.is_notify = True
        self.log = LoggerUtils.instance(self.__class__.__name__) # type: LoggerUtils
        self.retry_request = True
        self.fail_stop = 0
        self.is_less_log = False
        self.fail_no_skip = False
        self.proxy = None # '0.0.0.0:8000'
        self.is_use_proxies = False
        self.is_disable_verify = False
        self.cfscrape = None # type: CloudflareScraper
        self._pid = os.getpid()
        self._id = 'pid_' + self.__class__.__name__ + ' ' + str(self._pid)

        self.pool = None
        self.custom_callback = None

    @abc.abstractmethod
    def get_user_agent(self):
        pass

    @abc.abstractmethod
    def get(self, url, params:dict=None):
        pass

    @abc.abstractmethod
    def _get_kw(self, url, override_headers:dict=None, **kw):
        ''' RequestCommon. '''
        pass

    @abc.abstractmethod
    def _after_request(self, res, url):
        pass

    @abc.abstractmethod
    def _before_request(self, url):
        pass

    @abc.abstractmethod
    def get_output_path(self):
        pass

    @abc.abstractmethod
    def get_download_images_path(self, sub_path='', num_folder=False, is_favicon=False):
        pass

    @abc.abstractmethod
    def get_html_path(self, file_name=None):
        pass

    @abc.abstractmethod
    def notify(self, msg):
        pass

    @abc.abstractmethod
    def notify_error(self, msg):
        pass

    @abc.abstractmethod
    def enable_notify(self, enable=True):
        pass

    @abc.abstractmethod
    def html_to_desktop(self, html):
        pass

    def get_pid(self):
        return self._pid

    def get_id(self):
        return self._id

    def get_unused_proxy(self):
        return True

    def get_proxy(self):
        return None

    def enable_debug(self):
        self.is_debug = True

    def enable_log(self):
        self.is_log = True

    def enable_less_log(self):
        self.is_less_log = True

    def disable_notify(self):
        self.is_notify = False

    def enable_fail_no_skip(self):
        self.fail_no_skip = True

    def enable_cloudflare(self):
        import cfscrape

        self.cfscrape = cfscrape.create_scraper() # type: CloudflareScraper
        print('INFO: Enable cloudflare scrape')

    def disable_retry(self, value=False, fail_stop=0):
        self.retry_request = value
        self.fail_stop = fail_stop

    def get_timer(self, total, show_total=False, check_point=None):
        if show_total:
            print('INFO: Timer\'s total', total)
        return Timer(total, check_point=check_point)

    def get_redis(self): # type: () -> RedisConnect
        return RedisConnect.instance()

    def thread_pool(self, task_lst=None, callback=None, number_threads=None, multiple_process=False, maximum_req=0):
        from proxy.utils.TheadPool import ThreadPoolUtils

        def set_pool(pool, callback):
            self.pool = pool
            self.custom_callback = callback

        if task_lst:
            if not number_threads:
                number_threads = RequestBase.MAX_THREAD  # Default 20 threads

            pool = ThreadPoolUtils(request_utils=self)
            return pool.process(task_lst=task_lst, callback=callback, number_threads=number_threads, callback_getpool=set_pool, multiple_process=multiple_process, maximum_req=maximum_req)
        else:
            self.log.info('Empty task list')
            return 0

    def add_another_task(self, task, show_log=True):
        self.pool.add_task(self.custom_callback, task)
        msg = task if isinstance(task, str) else repr(task)
        if show_log:
            print('info: new %s - qsize: %d' % (msg, self.pool.get_pool_size()))
        else:
            print('+', end='', flush=True)