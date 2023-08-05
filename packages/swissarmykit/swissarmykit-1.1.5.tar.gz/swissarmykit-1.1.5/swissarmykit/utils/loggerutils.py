import sys
import time
import logging
from swissarmykit.lib.core import Singleton

@Singleton
class LoggerUtils:

    def __init__(self, file_name='log_', gui=None, datefmt='%d-%b %H:%M:%S'):
        rootLogger = logging.getLogger()
        self.logger = rootLogger
        self.gui = gui

        if not rootLogger.hasHandlers():
            time.strftime("%Y-%m-%d")

            if '/' not in file_name:
                try:
                    from swissarmykit.utils.fileutils import PathUtils
                    file_name = PathUtils.get_log_path() + '/' + file_name
                except Exception as e:
                    file_name = '/tmp/dist/log/' + file_name

            log_file = file_name + '_' + time.strftime("%Y-%m-%d") + '.log'

            logFormatter = logging.Formatter("%(asctime)s  %(levelname)s  %(message)s", datefmt=datefmt)

            rootLogger.setLevel(level=logging.INFO)

            fileHandler = logging.FileHandler(log_file, encoding='UTF-8')
            fileHandler.setFormatter(logFormatter)
            rootLogger.addHandler(fileHandler)

            consoleHandler = logging.StreamHandler()
            consoleHandler.setFormatter(logFormatter)
            rootLogger.addHandler(consoleHandler)

        if not self.gui:
            self.gui = gui

    def _get_text(self, text, *args):
        if args:
            return str(text) + ' ' + ' '.join([str(arg) for arg in args])
        return str(text)

    def inf(self, text, *args):
        self.info(text, *args)

    def info(self, text, *args):
        text = self._get_text(text, *args)
        self.logger.info(text)

        if self.gui:
            self.gui.send_text_info(text)

    def debug(self, text, *args):
        text = self._get_text(text, *args)

        self.logger.debug(text)
        if self.gui:
            self.gui.send_error_info(text)

    def error(self, text, *args):
        text = self._get_text(text, *args)

        self.logger.error(text)
        if self.gui:
            self.gui.send_error_info(text)

    def warn(self, text, *args):
        text = self._get_text(text, *args)

        self.warning(text)

    def warning(self, text, *args):
        text = self._get_text(text, *args)

        self.logger.warning(text)
        if self.gui:
            self.gui.send_error_info(text)

if __name__ == '__main__':
    log = LoggerUtils.instance()
    log.info('test', 'testd')