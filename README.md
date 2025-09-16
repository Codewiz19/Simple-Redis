# 🔑⚡ DSA-First Key-Value Store (C++ & Python)

A custom-built **Key-Value Store** inspired by Redis, written from scratch in **C++ and Python**, with a heavy focus on **Data Structures & Algorithms (DSA)**.
This project demonstrates low-level systems concepts — hashing, tries, concurrency, and networking — while staying practical with a simple client-server design.

---

## 🚀 Features

* **Custom Hash Table**

  * Separate chaining for collisions
  * Automatic resizing (maintains load factor \~0.75)
  * O(1) average time for `SET`, `GET`, `DEL`

* **Prefix Trie**

  * Supports efficient `SCAN prefix` queries
  * O(m + k) complexity (m = prefix length, k = matches)

* **(Optional) Skip List**

  * Ordered operations and range queries
  * O(log n) expected time for insert/search

* **Networking**

  * Simple TCP server
  * Commands: `SET key value`, `GET key`, `DEL key`, `SCAN prefix`
  * Custom lightweight text protocol

* **Concurrency**

  * Thread pool model (C++)
  * Lock-based thread safety
  * Python version uses `ThreadPoolExecutor` (I/O-bound due to GIL)

* **Persistence (optional)**

  * Append-only log for durability
  * Crash recovery by replaying log

---

## 🧩 System Architecture

```
+-------------------+
|   Client (CLI)    |
+-------------------+
         |
         v
+-------------------+
|  TCP Server Loop  |
+-------------------+
         |
   ---------------------
   |         |         |
   v         v         v
 Worker   Worker    Worker   ... (Thread Pool)
   |         |         |
   ---------------------
         |
         v
+-------------------+
|  KVStore (Core)   |
|  - HashMap        |
|  - Trie           |
|  - Skip List (*)  |
+-------------------+
```

(\*) Optional module

---

## ⚡ Usage

### Clone & Build

```bash
git clone https://github.com/your-username/dsa-kv-store.git
cd dsa-kv-store
```

### C++ Version

```bash
g++ -std=c++17 -pthread server.cpp -o kvstore
./kvstore
```

### Python Version

```bash
python3 server.py
```

---

## 💻 Example

```
> SET foo bar
+OK
> GET foo
bar
> DEL foo
+OK
> GET foo
(nil)
> SET apple red
> SET applet green
> SCAN app
["apple", "applet"]
```

---

## 🔍 Data Structures Deep Dive

### Hash Table

* **Chaining for collisions**
* **Resize strategy:** double capacity when load factor > 0.75
* **Amortized O(1)** inserts/lookups

### Prefix Trie

* **Prefix search in O(m)**
* **Used for SCAN/prefix queries**
* Prevents hash collisions for grouped lookups

### Skip List (Optional)

* **Probabilistic balanced structure**
* Easier concurrency than trees
* O(log n) expected ops

---

## 📊 Benchmarks

100k operations on a modern laptop (Python version):

```
SET: ~130,000 ops/sec
GET: ~220,000 ops/sec
```

C++ version achieves significantly higher throughput due to compiled performance.

 

## 📂 Project Structure

```
.
├── cpp/
│   ├── hashmap.hpp
│   ├── trie.hpp
│   ├── kvstore.hpp
│   └── server.cpp
├── python/
│   ├── hashmap.py
│   ├── trie.py
│   ├── kvstore.py
│   └── server.py
└── README.md
```

---

## 🛠️ Tech Stack

* **C++17** (STL, threads, sockets)
* **Python 3** (sockets, threading, asyncio optional)
* **Unix Sockets** for networking
* **DSA from scratch** (no external libraries)

---

## 🌟 Why This Project?

* Proves mastery in **core DSA**: hash tables, tries, skip lists
* Shows ability to **design concurrent systems**
* Demonstrates **network programming skills**
 

---

## 📜 License

MIT License © 2025 Your Name
