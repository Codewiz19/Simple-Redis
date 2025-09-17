#!/usr/bin/env python3
"""
bench_mt.py
Multi-threaded benchmark: each thread opens its own connection and performs ops.
"""
import socket, time, threading

HOST = "127.0.0.1"
PORT = 6379
THREADS = 8
OPS_PER_THREAD = 2000   # total ops = THREADS * OPS_PER_THREAD (reduce if too slow)

def worker(tid, ops):
    try:
        with socket.create_connection((HOST, PORT), timeout=5) as s:
            for i in range(ops):
                s.sendall((f"SET t{tid}-{i} v\n").encode())
                # read one-line response
                data = b""
                while True:
                    part = s.recv(4096)
                    if not part:
                        break
                    data += part
                    if b"\n" in data:
                        break
    except Exception as e:
        print(f"Thread {tid} error:", e)

def main():
    threads = []
    start = time.time()
    for t in range(THREADS):
        th = threading.Thread(target=worker, args=(t, OPS_PER_THREAD))
        th.start()
        threads.append(th)
    for th in threads:
        th.join()
    elapsed = time.time() - start
    total_ops = THREADS * OPS_PER_THREAD
    print(f"Total ops: {total_ops}, Throughput: {total_ops/elapsed:.0f} ops/sec, Time: {elapsed:.2f}s")

if __name__ == "__main__":
    print(f"Running multi-threaded benchmark: {THREADS} threads x {OPS_PER_THREAD} ops")
    main()
