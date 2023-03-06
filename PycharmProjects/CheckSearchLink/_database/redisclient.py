import redis

from config.settings import database_local, config


class RedisClient:

    def __init__(self, config):
        host = config['host']
        port = config['port']
        db = config['db']
        password = config['password']
        self.__db = redis.Redis(host=host, port=port, db=db, password=password)

    def _db(self):
        return self.__db

    def get_all_keys(self):
        return self.__db.keys()

    def get_type(self, name):
        return self.__db.type(name).decode(encoding='UTF-8')

    def get(self, key):
        return self.__db.get(key)

    def expire(self, key, expire):
        return self.__db.expire(key, expire)

    def rename(self, from_name, to_name):
        return self.__db.rename(from_name, to_name)

    def exists(self, key):
        return self.__db.exists(key)

    def search_key(self, pattern):
        return self.__db.keys(pattern)

    def get_multiple(self, keys):
        return self.__db.mget(keys)

    def get_multiple_by_pattern(self, pattern):
        keys = self.__db.keys(pattern)
        if keys:
            return self.__db.mget(keys)
        else:
            return []

    def delete(self, key):
        return self.__db.delete(key)

    def delete_multiple(self, keys):
        # return self.__db.delete(' '.join(str(x) for x in keys))
        return self.__db.delete(*keys)

    def delete_by_pattern(self, pattern):
        keys = self.__db.keys(pattern)
        return self.__db.delete(*keys)

    def sorted_add(self, key, value, score):
        return self.__db.zadd(key, value, score)

    def sorted_range_by_score(self, key, from_score, to_score):
        return self.__db.zrangebyscore(key, from_score, to_score)

    def sorted_rank(self, key, member):
        return self.__db.zrank(key, member)

    def sorted_reverse_range(self, key, start=0, end=-1):
        return self.__db.zrevrange(name=key, start=start, end=end)

    def sorted_range(self, key, start=0, end=-1):
        return self.__db.zrange(name=key, start=start, end=end)

    def sorted_range_with_score(self, key, start=0, end=-1, with_scores=False):
        return self.__db.zrange(name=key, start=start, end=end, withscores=with_scores)

    def sorted_remove(self, key, value):
        return self.__db.zrem(key, value)

    def sorted_remove_multiple(self, key, values):
        return self.__db.zrem(key, *values)

    def sorted_remove_range_by_rank(self, key, start=0, end=-1):
        return self.__db.zremrangebyrank(name=key, min=start, max=end)

    def sorted_remove_range_by_scores(self, key, start=0, end=-1):
        return self.__db.zremrangebyscore(name=key, min=start, max=end)

    def sorted_count(self, key, min='-inf', max='+inf'):
        return self.__db.zcount(key, min, max)

    def sorted_union_store(self, _dest, keys, aggregate=None):
        return self.__db.zunionstore(_dest, keys, aggregate)

    def list_push(self, key, value):
        return self.__db.lpush(key, value)

    def list_pop(self, key):
        return self.__db.lpop(key)

    def list_remove(self, key, value):
        return self.__db.lrem(key, 1, value)

    def list_range(self, key, start=0, end=-1):
        return self.__db.lrange(key, start, end)

    def list_full_item(self, key):
        n = self.__db.llen(key)
        return self.__db.lrange(key, 0, n)

    def list_trim(self, key, start=0, end=-1):
        return self.__db.ltrim(name=key, start=start, end=end)

    def list_len(self, key):
        return self.__db.llen(name=key)

    def hash_set(self, key, field, value):
        return self.__db.hset(key, field, value)

    def hash_set_not_exists(self, key, field, value):
        return self.__db.hsetnx(key, field, value)

    def hash_len(self, key):
        return self.__db.hlen(key)

    def hash_mset(self, key, mapping):
        return self.__db.hmset(key, mapping=mapping)

    def hash_exists(self, key, field):
        return self.__db.hexists(key, field)

    def hash_get(self, key, field):
        return self.__db.hget(key, field)

    def hash_get_all(self, key):
        return self.__db.hgetall(key)

    def hash_del(self, key, field):
        if type(field) is not list:
            field = [field]
        return self.__db.hdel(key, *field)

    def hash_keys(self, name):
        return self.__db.hkeys(name)

    def execute_command(self, command):
        return self.__db.execute_command(command)


class RedisQueues:

    def __init__(self, name, namespace='queue', config=None):
        host = config['host']
        port = config['port']
        db = config['db']
        password = config['password']

        self._rd = redis.Redis(host=host, port=port, db=db, password=password)
        self.key = "%s:%s" % (name, namespace)

    def get_all_item(self):
        n = self._rd.llen(self.key)
        return self._rd.lrange(self.key, 0, n)

    def enqueue(self, item):
        self._rd.lpush(self.key, item)

    def dequeue(self, item):
        self._rd.lrem(self.key, 1, item)

    def front(self):
        return self._rd.lrange(self.key, 0, 0)

    def rear(self):
        n = self._rd.llen(self.key)
        return self._rd.lrange(self.key, n - 1, n)

    def len_queue(self):
        return self._rd.llen(self.key)


data_redis_service = RedisQueues('list_links', 'queue', config)

data_redis_local = RedisQueues('list_links', 'queue', database_local)
