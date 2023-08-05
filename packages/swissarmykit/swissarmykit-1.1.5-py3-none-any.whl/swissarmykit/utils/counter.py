import logging
import time
from swissarmykit.lib.core import Singleton
try: from definitions_prod import *
except Exception as e: pass # Surpass error. Note: Create definitions_prod.py

@Singleton
class Counter:

    def __init__(self):
        self.offset = 0

    def count_offset(self):
        self.offset += 1

    def get_offset(self):
        return self.offset

if __name__ == '__main__':
    c = Counter.instance()
