# util/lru.py
"""A bounded least-recently-used cache.

Single-threaded by contract: instances are created per request handler and
never shared across threads. Callers are responsible for choosing a
capacity; a capacity of zero disables caching.
"""

from collections import OrderedDict


class LRUCache:
    def __init__(self, capacity):
        if capacity < 0:
            raise ValueError("capacity must be non-negative")
        self.capacity = capacity
        self._data = OrderedDict()
        self.hits = 0
        self.misses = 0

    def get(self, key, default=None):
        if key not in self._data:
            self.misses += 1
            return default
        self._data.move_to_end(key)
        self.hits += 1
        return self._data[key]

    def put(self, key, value):
        if self.capacity == 0:
            return
        if key in self._data:
            self._data.move_to_end(key)
        self._data[key] = value
        if len(self._data) > self.capacity:
            self._data.popitem(last=False)

    def __len__(self):
        return len(self._data)

    def __contains__(self, key):
        return key in self._data

    def clear(self):
        self._data.clear()
        self.hits = 0
        self.misses = 0
