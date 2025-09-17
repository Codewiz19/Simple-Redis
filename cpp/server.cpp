// Simple TCP server using POSIX sockets.
// Note: This is POSIX code (Linux / macOS / WSL). On native Windows use Winsock.
#include <arpa/inet.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <unistd.h>

#include <cstring>
#include <iostream>
#include <thread>
#include <vector>
#include <sstream>

#include "kvstore.hpp"

const int PORT = 6379;
const int BACKLOG = 16;
const int BUF_SIZE = 4096;

KVStore store;

void send_ok(int client_fd) {
    const char *ok = "+OK\n";
    send(client_fd, ok, strlen(ok), 0);
}

void send_nil(int client_fd) {
    const char *nil = "(nil)\n";
    send(client_fd, nil, strlen(nil), 0);
}

void handle_client(int client_fd) {
    char buf[BUF_SIZE];
    while (true) {
        ssize_t n = recv(client_fd, buf, BUF_SIZE - 1, 0);
        if (n <= 0) break;
        buf[n] = '\0';
        std::string data(buf);
        // Support multiple commands per recv by splitting on newline
        std::istringstream ss(data);
        std::string line;
        while (std::getline(ss, line)) {
            if (line.empty()) continue;
            // parse command
            std::istringstream ls(line);
            std::string cmd;
            ls >> cmd;
            if (cmd == "SET") {
                std::string key, value;
                ls >> key;
                // read rest as value (including spaces)
                std::string rest;
                std::getline(ls, rest);
                if (!rest.empty() && rest[0] == ' ') rest.erase(0,1);
                value = rest;
                store.set(key, value);
                send_ok(client_fd);
            } else if (cmd == "GET") {
                std::string key; ls >> key;
                auto v = store.get(key);
                if (v) {
                    std::string out = *v + "\n";
                    send(client_fd, out.c_str(), out.size(), 0);
                } else {
                    send_nil(client_fd);
                }
            } else if (cmd == "DEL") {
                std::string key; ls >> key;
                bool removed = store.del(key);
                std::string out = removed ? "+OK\n" : "(nil)\n";
                send(client_fd, out.c_str(), out.size(), 0);
            } else if (cmd == "SCAN") {
                std::string prefix; ls >> prefix;
                auto keys = store.scan(prefix);
                std::string out;
                for (auto &k : keys) { out += k + "\n"; }
                if (out.empty()) out = "(nil)\n";
                send(client_fd, out.c_str(), out.size(), 0);
            } else {
                std::string msg = "ERR unknown command\n";
                send(client_fd, msg.c_str(), msg.size(), 0);
            }
        }
    }
    close(client_fd);
}

int main() {
    int server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (server_fd == -1) { perror("socket"); return 1; }

    int opt = 1;
    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

    sockaddr_in addr{};
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = INADDR_ANY;
    addr.sin_port = htons(PORT);

    if (bind(server_fd, (sockaddr*)&addr, sizeof(addr)) == -1) { perror("bind"); return 2; }
    if (listen(server_fd, BACKLOG) == -1) { perror("listen"); return 3; }

    std::cout << "KVStore server listening on port " << PORT << "...\n";

    while (true) {
        sockaddr_in client_addr;
        socklen_t client_len = sizeof(client_addr);
        int client_fd = accept(server_fd, (sockaddr*)&client_addr, &client_len);
        if (client_fd == -1) {
            perror("accept");
            continue;
        }
        // spawn thread to handle client (detached)
        std::thread t(handle_client, client_fd);
        t.detach();
    }

    close(server_fd);
    return 0;
}
