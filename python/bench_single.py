#!/usr/bin/env python3
"""
bench_single.py
Single-connection benchmark: reuses one TCP connection to the KV server.
Measures SET then GET throughput.
"""
import socket, time

HOST = "127.0.0.1"
PORT = 6379
N = 20000  # number of operations (reduce to 5000 if slow)

def send_line(s, line: str):
    s.sendall((line + "\n").encode())
    # read one line response
    data = b""
    while True:
        part = s.recv(4096)
        if not part:
            break
        data += part
        if b"\n" in data:
            break
    return data.decode().strip()

def bench_set_get(n):
    # Warm-up connection
    with socket.create_connection((HOST, PORT), timeout=5) as s:
        # small warmup
        for i in range(50):
            send_line(s, f"SET warm{i} v")
    # SET benchmark (reuse single connection)
    start = time.time()
    with socket.create_connection((HOST, PORT), timeout=5) as s:
        for i in range(n):
            send_line(s, f"SET k{i} v{i}")
    elapsed_set = time.time() - start

    # GET benchmark
    start = time.time()
    with socket.create_connection((HOST, PORT), timeout=5) as s:
        for i in range(n):
            send_line(s, f"GET k{i}")
    elapsed_get = time.time() - start

    print(f"SET: {n/elapsed_set:.0f} ops/sec ({elapsed_set:.2f}s total)")
    print(f"GET: {n/elapsed_get:.0f} ops/sec ({elapsed_get:.2f}s total)")

if __name__ == "__main__":
    print("Running single-connection benchmark. N =", N)
    bench_set_get(N)
