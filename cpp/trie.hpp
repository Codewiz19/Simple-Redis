#pragma once
#include <unordered_map>
#include <memory>
#include <string>
#include <vector>
#include <mutex>

class Trie {
    struct Node {
        std::unordered_map<char, std::unique_ptr<Node>> children;
        bool is_end = false;
    };
public:
    Trie() : root_(std::make_unique<Node>()) {}

    void insert(const std::string &s) {
        std::lock_guard<std::mutex> lg(mutex_);
        Node *cur = root_.get();
        for (char c : s) {
            if (!cur->children.count(c)) cur->children[c] = std::make_unique<Node>();
            cur = cur->children[c].get();
        }
        cur->is_end = true;
    }

    bool contains(const std::string &s) {
        std::lock_guard<std::mutex> lg(mutex_);
        Node *cur = root_.get();
        for (char c : s) {
            if (!cur->children.count(c)) return false;
            cur = cur->children[c].get();
        }
        return cur->is_end;
    }

    // Remove: returns true if removed
    bool remove(const std::string &s) {
        std::lock_guard<std::mutex> lg(mutex_);
        return remove_rec(root_.get(), s, 0);
    }

    // Return all keys with prefix
    std::vector<std::string> scan_prefix(const std::string &prefix) {
        std::lock_guard<std::mutex> lg(mutex_);
        std::vector<std::string> results;
        Node *cur = root_.get();
        for (char c : prefix) {
            if (!cur->children.count(c)) return results;
            cur = cur->children[c].get();
        }
        std::string acc;
        dfs_collect(cur, prefix, results);
        return results;
    }

private:
    bool remove_rec(Node *node, const std::string &s, size_t depth) {
        if (!node) return false;
        if (depth == s.size()) {
            if (!node->is_end) return false;
            node->is_end = false;
            return node->children.empty();
        }
        char c = s[depth];
        auto it = node->children.find(c);
        if (it == node->children.end()) return false;
        bool shouldDeleteChild = remove_rec(it->second.get(), s, depth + 1);
        if (shouldDeleteChild) {
            node->children.erase(c);
            return !node->is_end && node->children.empty();
        }
        return false;
    }

    void dfs_collect(Node *node, const std::string &prefix, std::vector<std::string> &out) {
        if (!node) return;
        if (node->is_end) out.push_back(prefix);
        for (auto &kv : node->children) {
            dfs_collect(kv.second.get(), prefix + kv.first, out);
        }
    }

    std::unique_ptr<Node> root_;
    std::mutex mutex_;
};
