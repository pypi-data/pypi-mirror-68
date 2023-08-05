import redis
from swissarmykit.lib.core import Singleton

try: from definitions_prod import *
except Exception as e: pass # Surpass error. Note: Create definitions_prod.py


@Singleton
class RedisConnect():

    def __init__(self, config='redis'):
        try:
            self.redis = redis.Redis(**appConfig.config.get(config))
        except Exception as e:
            self.log.error(e)

    def get_restrict(self, config='redis'):
        return redis.StrictRedis(**appConfig.config.get(config))

    def get(self, key):
        return self.redis.get(key)

    def set(self, key, value, ex=3600):
        self.redis.set(key, value, ex=ex)

    def delete(self, key):
        self.redis.delete(key)

    def delete_namespace(self, ns):
       prefix = '%s:*' % ns
       for key in self.redis.scan_iter(prefix):
           self.delete(key)

    def lpush(self, name, value):
        self.redis.lpush(name, value)

    def get_list(self, name):
        return self.redis.lrange(name, 0, -1)

