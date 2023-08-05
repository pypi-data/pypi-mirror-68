import time

from swissarmykit.utils.loggerutils import LoggerUtils
from swissarmykit.lib.core import Singleton
try: from definitions_prod import *
except Exception as e: pass

@Singleton
class Timer:

    def __init__(self, total=0, file_name='timer_', check_point=None):
        self.log = LoggerUtils.instance(file_name) # type: LoggerUtils
        self.cache = appConfig.get_process_tmp()
        self.t0 = time.time()
        self.prev_t0 = self.t0
        self.title = None
        self.total_task = total
        self.remain_task = total

        self.msg = ''
        self._id = 'pid_timer ' + str(os.getpid())
        self.check_point = check_point if check_point else 1000

    def reset(self, total=0):
        self.t0 = time.time()
        self.total_task = total
        self.remain_task = total

    def check(self, item=None, idx=None):
        self.remain_task -= 1
        # print('.', end='', flush=True)

        if self.remain_task % self.check_point == 0:
            t1 = time.time()
            time_spent = (t1 - self.t0) / 60

            extra_msg = ''
            if item:
                extra_msg = ' - (id: %s url: %s)' % (str(item.id), item.url)
            if idx:
                extra_msg += ' Idx: %d' % idx

            if self.total_task:
                done_task = self.total_task - self.remain_task
                time_eta = self.remain_task * time_spent / (done_task + 1) # Avoid divide by 0
                self.msg = "     {:4d}% tasks - eta: {} - et: {} - remain: {}  {}".format(
                    round(done_task * 100 / self.total_task), self.convert_mm_2_hh_mm(time_eta), self.convert_mm_2_hh_mm(time_spent), self.remain_task, extra_msg)
            else:
                self.msg = "     et: {} - total: {} tasks. {}".format(self.convert_mm_2_hh_mm(time_spent), abs(self.remain_task), extra_msg)

            self.log.info(self.msg)

        if self.remain_task % 10000:
            self.cache.save_attr(self._id, attr={'value': {'message': self.msg}})

    def done(self):
        self.spent()

    def start(self, title=None):
        self.title = title
        self.prev_t0 = time.time()

    def spent(self):
        t1 = time.time()
        time_spent = (t1 - self.prev_t0) / 60
        if self.title:
            self.log.info("- {}. et: {}m.".format(self.title, round(time_spent, 2)))
            self.title = None
        else:
            self.log.info("et: {}m.".format(round(time_spent, 2)))

    def convert_mm_2_hh_mm(self, minutes):
        return "%dh %02dm" % (round(minutes / 60), minutes % 60)


if __name__ == '__main__':
    timer = Timer.instance()
    for i in range(2001):
        timer.check()
