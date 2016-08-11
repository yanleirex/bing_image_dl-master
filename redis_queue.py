#!/usr/bin/env python
# -*- coding:utf-8 -*-
import redis


class RedisQueue(object):
    """Simple Queue with Redis Backend"""

    def __init__(self, name, namespace='queue', **redis_kwargs):
        """The default connection parameters are:host='localhost', port=6379, db=0"""
        self._db = redis.Redis(**redis_kwargs)
        self.key = '%s:%s' % (namespace, name)
        self.set_key = '%s:%s_set' % (namespace, name)

    def qsize(self):
        """Return the approximate size of the queue"""
        return self._db.llen(self.key)

    def set_size(self):
        """Return set size"""
        return self._db.scard(self.set_key)

    def empty(self):
        """Return True if the queue is empty, False otherwise"""
        return self.qsize() == 0

    def set_empty(self):
        """Return True if the set is empty, False othersize"""
        return self.set_size() == 0

    def put(self, item):
        """Put item into queue
        :param item:
        """
        self._db.rpush(self.key, item)

    def get(self, block=True, timeout=None):
        """Remove and return an item from the queue
        If optional args block is true and timeout is None(default),
        block if necessary until an item is available.
        :param timeout:
        :param block: """
        if block:
            item = self._db.blpop(self.key, timeout=timeout)
        else:
            item = self._db.lpop(self.key)

        if item:
            item = item[1]
        return item

    def get_nowait(self):
        """Equivalent to get(False)"""
        return self.get(False)

    def set_add(self, item):
        """Add item into set
        :param item:
        """
        self._db.sadd(self.set_key, item)

    def set_pop(self):
        """get an item form set"""
        return self._db.spop(self.set_key)

    def set_is_member(self, item):
        """Check item is in the set
        :param item"""
        return True if self._db.sismember(self.set_key, item) else False


if __name__ == "__main__":
    q = RedisQueue('test')
    q.set_add('hello')
    q.set_add('hello')
    if q.set_is_member('hello'):
        print "True"
    # print q.set_pop()
