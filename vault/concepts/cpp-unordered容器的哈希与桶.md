---
title: unordered 容器的哈希与桶
tags: [cpp, unordered, hash, bucket, load-factor, collision, custom-hash]
aliases: [哈希容器实现, 桶, load factor, 碰撞, 自定义哈希函数]
created: 2026-04-04
updated: 2026-04-04
---

# unordered 容器的哈希与桶

理解 `unordered_map` 的内部机制——哈希函数、桶、负载因子——才能写出高性能的哈希容器代码。

## 内部结构

```
unordered_map 内部布局：

key → hash(key) → bucket_index = hash % bucket_count
                    ↓
bucket 0: [key1, val1] → [key2, val2]  (链式冲突)
bucket 1: [key3, val3]
bucket 2: (空)
bucket 3: [key4, val4] → [key5, val5] → [key6, val6]
...

负载因子 = size / bucket_count
当 负载因子 > max_load_factor（默认1.0）时 rehash
```

## 哈希函数质量

```cpp
// ❌ 差的哈希函数：导致大量碰撞
struct BadHash {
    size_t operator()(int x) const { return x % 100; }  // 只用 100 个桶
};

// ✅ 好的哈希函数：均匀分布
struct GoodHash {
    size_t operator()(int x) const {
        return std::hash<int>{}(x);  // 标准库哈希通常够好
    }
};

// 组合哈希（用于复合 key）
struct PairHash {
    size_t operator()(const std::pair<int, int>& p) const {
        auto h1 = std::hash<int>{}(p.first);
        auto h2 = std::hash<int>{}(p.second);
        return h1 ^ (h2 * 0x9e3779b9 + (h1 << 6) + (h1 >> 2));  // boost 的 hash_combine
    }
};
```

## 桶管理

```cpp
std::unordered_map<int, int> m;

// 预分配桶（避免 rehash）
m.reserve(1000);  // 确保桶数足够 1000 个元素而不 rehash

// 查看内部状态
m.bucket_count();       // 当前桶数
m.load_factor();        // size / bucket_count
m.max_load_factor();    // 最大负载因子（默认 1.0）
m.bucket_size(0);       // 第 0 个桶中的元素数

// 设置最大负载因子
m.max_load_factor(0.75);  // 更低 → 冲突更少 → 更快，但内存更多
```

## 关键要点

> 好的哈希函数 = 均匀分布 + 快速计算。自定义类型必须提供哈希函数，否则用 `std::hash` 默认实现。

> 预调用 `reserve(n)` 避免多次 rehash——rehash 涉及重新分配所有元素，代价很高。

## 相关模式 / 关联

- [[cpp-unordered-map]] — unordered_map 使用
- [[算法-哈希表]] — 哈希表原理
