# Simple trie with thread-safety
import threading

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
        self.lock = threading.Lock()

    def insert(self, key: str):
        with self.lock:
            node = self.root
            for ch in key:
                if ch not in node.children:
                    node.children[ch] = TrieNode()
                node = node.children[ch]
            node.is_end = True

    def contains(self, key: str) -> bool:
        with self.lock:
            node = self.root
            for ch in key:
                if ch not in node.children:
                    return False
                node = node.children[ch]
            return node.is_end

    def remove(self, key: str) -> bool:
        with self.lock:
            return self._remove(self.root, key, 0)

    def _remove(self, node, key, depth):
        if not node:
            return False
        if depth == len(key):
            if not node.is_end:
                return False
            node.is_end = False
            return len(node.children) == 0
        ch = key[depth]
        if ch not in node.children:
            return False
        should_delete = self._remove(node.children[ch], key, depth+1)
        if should_delete:
            del node.children[ch]
            return (not node.is_end) and (len(node.children) == 0)
        return False

    def scan_prefix(self, prefix: str):
        with self.lock:
            node = self.root
            for ch in prefix:
                if ch not in node.children:
                    return []
                node = node.children[ch]
            results = []
            self._dfs(node, prefix, results)
            return results

    def _dfs(self, node, path, out):
        if node.is_end:
            out.append(path)
        for ch, child in node.children.items():
            self._dfs(child, path + ch, out)
