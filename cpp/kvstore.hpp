#pragma once
#include "hashmap.hpp"
#include "trie.hpp"
#include <optional>
#include <string>
#include <vector>
#include <mutex>

class KVStore {
public:
    KVStore() = default;

    // Set key to value (thread-safe)
    void set(const std::string &key, const std::string &value) {
        // We keep operations atomic at KVStore level
        {
            map_.set(key, value);
            trie_.insert(key);
        }
    }

    // Get value or std::nullopt
    std::optional<std::string> get(const std::string &key) {
        return map_.get(key);
    }

    // Delete key; return true if removed
    bool del(const std::string &key) {
        bool removed = map_.del(key);
        if (removed) trie_.remove(key);
        return removed;
    }

    // Return matching keys for prefix
    std::vector<std::string> scan(const std::string &prefix) {
        return trie_.scan_prefix(prefix);
    }

private:
    HashMap map_;
    Trie trie_;
};
