# Simple chaining hash map with resizing and thread-safety
import threading

class HashMap:
    def __init__(self, capacity=8):
        self.capacity = capacity
        self.size = 0
        self.buckets = [[] for _ in range(capacity)]
        self.lock = threading.Lock()
        self.max_load = 0.75

    def _rehash(self):
        old = self.buckets
        self.capacity *= 2
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0
        for bucket in old:
            for k,v in bucket:
                self.set(k, v)

    def set(self, key, value):
        with self.lock:
            idx = hash(key) % self.capacity
            for i, (k,_) in enumerate(self.buckets[idx]):
                if k == key:
                    self.buckets[idx][i] = (key, value)
                    return
            self.buckets[idx].append((key, value))
            self.size += 1
            if self.size / self.capacity > self.max_load:
                self._rehash()

    def get(self, key):
        with self.lock:
            idx = hash(key) % self.capacity
            for k, v in self.buckets[idx]:
                if k == key:
                    return v
            return None

    def delete(self, key):
        with self.lock:
            idx = hash(key) % self.capacity
            bucket = self.buckets[idx]
            for i, (k,_) in enumerate(bucket):
                if k == key:
                    bucket.pop(i)
                    self.size -= 1
                    return True
            return False
