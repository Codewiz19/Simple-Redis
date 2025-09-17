# client.py - interactive TCP client for the KV server
import socket

HOST = '127.0.0.1'
PORT = 6379

def send(cmd: str):
    try:
        with socket.create_connection((HOST, PORT), timeout=2) as s:
            s.sendall((cmd.strip() + "\n").encode())
            data = b""
            # read a bit (server responds line-by-line)
            while True:
                part = s.recv(4096)
                if not part:
                    break
                data += part
                if b"\n" in data:
                    break
            print(data.decode(), end="")
    except Exception as e:
        print("ERROR:", e)

if __name__ == "__main__":
    print("Simple client. Type commands (SET/GET/DEL/SCAN). Type quit to exit.")
    while True:
        try:
            cmd = input("> ")
        except EOFError:
            break
        if not cmd or cmd.lower() in ("q", "quit", "exit"):
            break
        send(cmd)
