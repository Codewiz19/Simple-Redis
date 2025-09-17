from .hashmap import HashMap
from .trie import Trie

class KVStore:
    def __init__(self):
        self.map = HashMap()
        self.trie = Trie()

    def set(self, key, value):
        self.map.set(key, value)
        self.trie.insert(key)

    def get(self, key):
        return self.map.get(key)

    def delete(self, key):
        removed = self.map.delete(key)
        if removed:
            self.trie.remove(key)
        return removed

    def scan(self, prefix):
        return self.trie.scan_prefix(prefix)
