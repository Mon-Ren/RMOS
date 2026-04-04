---
title: 编译期字符串哈希
tags: [cpp, constexpr, string-hash, compile-time, switch-on-string, hash]
aliases: [编译期哈希, 字符串哈希, switch on string, compile-time hash, FNV]
created: 2026-04-04
updated: 2026-04-04
---

# 编译期字符串哈希

编译期将字符串哈希为整数——让 `switch` 语句能处理字符串匹配，零运行时开销。

## 实现

```cpp
#include <cstdint>

// FNV-1a 哈希
constexpr uint64_t fnv1a(const char* str, size_t len) {
    uint64_t hash = 14695981039346656037ULL;  // FNV offset basis
    for (size_t i = 0; i < len; ++i) {
        hash ^= static_cast<uint64_t>(str[i]);
        hash *= 1099511628211ULL;             // FNV prime
    }
    return hash;
}

// 字面量版本
constexpr uint64_t operator""_hash(const char* str, size_t len) {
    return fnv1a(str, len);
}

// 使用
constexpr auto CONFIG_KEY = "config"_hash;  // 编译期计算
constexpr auto DEBUG_KEY  = "debug"_hash;
```

## switch on string

```cpp
void handle(const std::string& cmd) {
    switch (fnv1a(cmd.c_str(), cmd.size())) {
        case "start"_hash:
            start_service();
            break;
        case "stop"_hash:
            stop_service();
            break;
        case "status"_hash:
            show_status();
            break;
        default:
            unknown_command(cmd);
    }
}
```

## 防碰撞

```cpp
// 编译期检查：确保哈希不碰撞
static_assert("start"_hash != "stop"_hash);
static_assert("alpha"_hash != "beta"_hash);

// 如果碰撞，可以：
// 1. 改用更长的哈希（128位）
// 2. 在 case 中加运行时 string 比较
case "ambiguous"_hash:
    if (cmd != "ambiguous") break;  // 防碰撞检查
    // ...
```

## 关键要点

> 编译期哈希将字符串比较的 O(n) 降为整数比较的 O(1)——但要注意哈希碰撞风险。在 case 分支中加运行时 string 比较是防碰撞的标准做法。

> FNV-1a 是简单快速的非加密哈希——加密场景用 SHA-256 等。

## 相关模式 / 关联

- [[cpp-自定义字面量]] — _hash 后缀
- [[cpp-constexpr与constexpr深入]] — 编译期计算
