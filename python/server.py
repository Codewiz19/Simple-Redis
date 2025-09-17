#!/usr/bin/env python3
import socket
import threading
from hashmap import HashMap
from trie import Trie

# Simple KV store using the modules above (non-package import for ease)
class KVStore:
    def __init__(self):
        self.map = HashMap()
        self.trie = Trie()

    def set(self, k, v):
        self.map.set(k, v)
        self.trie.insert(k)

    def get(self, k):
        return self.map.get(k)

    def delete(self, k):
        removed = self.map.delete(k)
        if removed:
            self.trie.remove(k)
        return removed

    def scan(self, prefix):
        return self.trie.scan_prefix(prefix)

store = KVStore()

HOST = '0.0.0.0'
PORT = 6379

def handle_conn(conn, addr):
    with conn:
        data = b""
        while True:
            chunk = conn.recv(4096)
            if not chunk:
                break
            data += chunk
            # process lines
            while b"\n" in data:
                line, data = data.split(b"\n", 1)
                line = line.decode().strip()
                if not line:
                    continue
                parts = line.split(" ", 2)
                cmd = parts[0].upper()
                if cmd == "SET":
                    if len(parts) < 3:
                        conn.sendall(b"ERR usage: SET key value\n")
                        continue
                    key = parts[1]
                    value = parts[2]
                    store.set(key, value)
                    conn.sendall(b"+OK\n")
                elif cmd == "GET":
                    if len(parts) < 2:
                        conn.sendall(b"ERR usage: GET key\n"); continue
                    key = parts[1]
                    v = store.get(key)
                    if v is None:
                        conn.sendall(b"(nil)\n")
                    else:
                        conn.sendall((v + "\n").encode())
                elif cmd == "DEL":
                    if len(parts) < 2:
                        conn.sendall(b"ERR usage: DEL key\n"); continue
                    key = parts[1]
                    removed = store.delete(key)
                    conn.sendall(b"+OK\n" if removed else b"(nil)\n")
                elif cmd == "SCAN":
                    if len(parts) < 2:
                        conn.sendall(b"ERR usage: SCAN prefix\n"); continue
                    prefix = parts[1]
                    keys = store.scan(prefix)
                    if not keys:
                        conn.sendall(b"(nil)\n")
                    else:
                        for k in keys:
                            conn.sendall((k + "\n").encode())
                else:
                    conn.sendall(b"ERR unknown command\n")

def serve():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(8)
    print(f"KVStore (python) listening on {HOST}:{PORT}")
    try:
        while True:
            conn, addr = s.accept()
            t = threading.Thread(target=handle_conn, args=(conn, addr), daemon=True)
            t.start()
    finally:
        s.close()

if __name__ == "__main__":
    serve()
