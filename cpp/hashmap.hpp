#pragma once
#include <vector>
#include <list>
#include <string>
#include <functional>
#include <mutex>
#include <optional>

class HashMap {
public:
    using Key = std::string;
    using Value = std::string;

    HashMap(size_t capacity = 8) : buckets_(capacity), size_(0) {}

    void set(const Key &key, const Value &value) {
        std::lock_guard<std::mutex> lg(mutex_);
        insert_or_assign(key, value);
        if ((double)size_ / buckets_.size() > max_load_) rehash();
    }

    std::optional<Value> get(const Key &key) {
        std::lock_guard<std::mutex> lg(mutex_);
        size_t idx = bucket_index(key);
        for (auto &p : buckets_[idx]) if (p.first == key) return p.second;
        return std::nullopt;
    }

    bool del(const Key &key) {
        std::lock_guard<std::mutex> lg(mutex_);
        size_t idx = bucket_index(key);
        auto &bucket = buckets_[idx];
        for (auto it = bucket.begin(); it != bucket.end(); ++it) {
            if (it->first == key) {
                bucket.erase(it);
                --size_;
                return true;
            }
        }
        return false;
    }

    size_t size() const {
        std::lock_guard<std::mutex> lg(mutex_);
        return size_;
    }

private:
    void insert_or_assign(const Key &key, const Value &value) {
        size_t idx = bucket_index(key);
        for (auto &p : buckets_[idx]) {
            if (p.first == key) { p.second = value; return; }
        }
        buckets_[idx].emplace_back(key, value);
        ++size_;
    }

    size_t bucket_index(const Key &key) const {
        return std::hash<Key>{}(key) % buckets_.size();
    }

    void rehash() {
        size_t newcap = buckets_.size() * 2;
        std::vector<std::list<std::pair<Key,Value>>> newb(newcap);
        for (auto &bucket : buckets_) {
            for (auto &p : bucket) {
                size_t idx = std::hash<Key>{}(p.first) % newcap;
                newb[idx].emplace_back(p.first, p.second);
            }
        }
        buckets_.swap(newb);
    }

    mutable std::mutex mutex_;
    std::vector<std::list<std::pair<Key,Value>>> buckets_;
    size_t size_;
    const double max_load_ = 0.75;
};
