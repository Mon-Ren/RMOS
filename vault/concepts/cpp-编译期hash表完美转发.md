---
title: 编译期完美哈希
tags: [cpp, constexpr, perfect-hash, gperf, compile-time]
aliases: [完美哈希, 编译期哈希表, gperf C++]
created: 2026-04-05
updated: 2026-04-05
---

# 编译期完美哈希

**一句话概述：** 当键集合在编译期已知时（比如命令字符串、配置键），可以用编译期计算生成完美哈希函数——保证零碰撞、O(1) 查找。比通用哈希表更快、更省内存。

## 实现思路

```cpp
#include <string_view>
#include <array>
#include <algorithm>

// 编译期已知的键集合
constexpr std::array<const char*, 5> keys = {"start", "stop", "pause", "resume", "reset"};

// 编译期哈希 + 碰撞检测
constexpr size_t hash_key(std::string_view s, size_t seed = 0) {
    for (char c : s) seed = seed * 31 + static_cast<unsigned char>(c);
    return seed;
}

constexpr size_t find_key_index(std::string_view query) {
    for (size_t i = 0; i < keys.size(); ++i) {
        if (keys[i] == query) return i;
    }
    return static_cast<size_t>(-1);  // 未找到
}

// 编译期生成跳转表
template <typename F>
void dispatch(std::string_view cmd, F&& handler) {
    switch (hash_key(cmd)) {
        case hash_key("start"):  handler.start(); break;
        case hash_key("stop"):   handler.stop(); break;
        case hash_key("pause"):  handler.pause(); break;
        case hash_key("resume"): handler.resume(); break;
        case hash_key("reset"):  handler.reset(); break;
        default: handler.unknown(cmd);
    }
}
```

## 关键要点

> 编译期完美哈希适合键数 < 100 的场景。超过 100 个键建议用 gperf 工具生成，或退回到运行时哈希表。

## 相关模式 / 关联

- [[cpp-编译期字符串hash与switch-string]] — 编译期 hash
- [[cpp-编译期计算与constexpr深入]] — constexpr
- [[cpp-算法-哈希表]] — 哈希表原理
