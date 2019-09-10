from abc import abstractmethod, ABC
import numpy as np

__all__ = ['LRUCache', 'FIFOCache', 'LFUCache', 'RRCache']

class Cache(ABC):
    def __init__(self, size):
        self._size = size
        self._storage = {}

    @property
    def capacity(self): return self._size

    @property
    def usage(self): return len(self._storage)
    
    def __len__(self): return self.usage

    def __contains__(self, key):
        return key in self._storage
    
    def __repr__(self):
        return self._storage.__repr__()
    
    @abstractmethod
    def clear(self): pass

    @abstractmethod
    def __getitem__(self, key): pass
    
    @abstractmethod
    def __setitem__(self, key, value): pass


class LRUCache(Cache):
    def __init__(self, size=10):
        self._priority = []
        super( LRUCache, self ).__init__(size)

    def clear(self):
        self._storage = {}
        self._priority = []
    
    def __getitem__(self, key):
        if key not in self._priority:
            raise KeyError
        self._priority.remove(key)
        self._priority.insert(0, key)
        return self._storage[ key ]
    
    def __setitem__(self, key, value):
        if key in self._priority:
            self._priority.remove(key)
            del self._storage[key]
        if len(self._priority) == self.capacity:
            rk = self._priority.pop()
            del self._storage[rk]
        self._priority.insert(0, key)
        self._storage[ key ] = value


class FIFOCache(Cache):
    def __init__(self, size=10):
        self._priority = []
        super( FIFOCache, self ).__init__(size)

    def clear(self):
        self._storage = {}
        self._priority = []
    
    def __getitem__(self, key):
        if key not in self._priority:
            raise KeyError
        return self._storage[ key ]

    def __setitem__(self, key, value):
        if key in self._priority:
            self._priority.remove(key)
            del self._storage[key]
        if len(self._priority) == self.capacity:
            rk = self._priority.pop()
            del self._storage[rk]
        self._priority.insert(0, key)
        self._storage[ key ] = value


class LFUCache(Cache):
    def __init__(self, size=10):
        self._frequency = {}
        super( LFUCache, self ).__init__(size)

    def clear(self):
        self._storage = {}
        self._frequency = {}
    
    def __getitem__(self, key):
        if key not in self._storage:
            raise KeyError
        self._frequency[key] += 1
        return self._storage[ key ]

    def __setitem__(self, key, value):
        if len(self._storage) == self.capacity and key not in self:
            rk = min(self._frequency.items(), key=lambda x:x[1])[0]
            del self._storage[rk]
            del self._frequency[rk]
        self._frequency[key] = 1
        self._storage[key] = value

class RRCache(Cache):
    def __init__(self, size=10, seed=None):
        self._state = np.random.RandomState(seed)
        super( RRCache, self ).__init__(size)

    def clear(self):
        self._storage = {} 
    
    def __getitem__(self, key):
        if key not in self._storage:
            raise KeyError
        return self._storage[ key ]

    def __setitem__(self, key, value):
        if len(self._storage) == self.capacity and key not in self:
            rk = self._state.choice( list(self._storage.keys()) )
            del self._storage[rk]
        self._storage[key] = value


