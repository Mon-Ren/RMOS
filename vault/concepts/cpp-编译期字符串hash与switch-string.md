---
title: 编译期字符串 hash 与 switch-string
tags: [cpp, constexpr, string-hash, fnv1a, compile-time]
aliases: [编译期 hash, switch on string, FNV-1a, 字符串 hash]
created: 2026-04-05
updated: 2026-04-05
---

# 编译期字符串 hash 与 switch-string

**一句话概述：** C++ 的 switch 不支持 string，但可以在编译期把字符串 hash 成整数，然后 switch 整数。关键是要用 `if constexpr` 或 `consteval` 保证 hash 冲突在编译期被捕获——两个不同的字符串 hash 到同一个值就报编译错误。

## 意图与场景

- 替代 `if-else if` 链式字符串比较
- 命令行参数解析、协议分发、日志级别判断
- 配置文件 key 的高效匹配

## 基础实现：FNV-1a hash

```cpp
#include <cstdint>
#include <string_view>

// FNV-1a：简单、快速、编译期友好
// 64 位版本，碰撞概率足够低（2^64 空间）
constexpr uint64_t fnv1a(std::string_view str) {
    uint64_t hash = 0xcbf29ce484222325ULL;  // FNV offset basis
    for (char c : str) {
        hash ^= static_cast<uint64_t>(c);
        hash *= 0x100000001b3ULL;            // FNV prime
    }
    return hash;
}

// 编译期验证：static_assert 保证函数确实是 constexpr
static_assert(fnv1a("hello") == fnv1a("hello"));
static_assert(fnv1a("hello") != fnv1a("world"));
```

## 安全的 switch-string 实现

```cpp
#include <cstdint>
#include <string_view>
#include <stdexcept>

constexpr uint64_t hash(std::string_view s) {
    uint64_t h = 0xcbf29ce484222325ULL;
    for (char c : s) {
        h ^= static_cast<uint64_t>(c);
        h *= 0x100000001b3ULL;
    }
    return h;
}

// 编译期碰撞检测
// 如果两个不同的字符串 hash 到同一个值，编译失败
template <std::string_view const&... Strings>
struct CheckNoCollision {
    static constexpr bool check() {
        constexpr uint64_t hashes[] = { hash(Strings)... };
        for (size_t i = 0; i < sizeof...(Strings); ++i) {
            for (size_t j = i + 1; j < sizeof...(Strings); ++j) {
                if (hashes[i] == hashes[j]) {
                    // 编译期检测到碰撞！
                    // （实际中 FNV-1a 碰撞概率极低）
                    return false;
                }
            }
        }
        return true;
    }
    static_assert(check(), "Hash collision detected at compile time!");
};

// 实际使用
void handle_command(std::string_view cmd) {
    switch (hash(cmd)) {
        case hash("start"):    // 编译期计算
            // 启动服务
            break;
        case hash("stop"):
            // 停止服务
            break;
        case hash("restart"):
            // 重启服务
            break;
        case hash("status"):
            // 查看状态
            break;
        default:
            throw std::invalid_argument("Unknown command");
    }
}
```

## C++20 consteval 版本（更安全）

```cpp
// consteval 保证：这个函数必须在编译期求值
// 如果无法在编译期求值，编译错误（而不是静默退化为运行时）
consteval uint64_t hash(const char* str, size_t len) {
    uint64_t h = 0xcbf29ce484222325ULL;
    for (size_t i = 0; i < len; ++i) {
        h ^= static_cast<uint64_t>(str[i]);
        h *= 0x100000001b3ULL;
    }
    return h;
}

// 用户自定义字面量
consteval uint64_t operator""_hash(const char* str, size_t len) {
    return hash(str, len);
}

// 使用
void dispatch(std::string_view msg_type) {
    switch (hash(msg_type.data(), msg_type.size())) {
        case "PING"_hash:  handle_ping(); break;
        case "PONG"_hash:  handle_pong(); break;
        case "DATA"_hash:  handle_data(); break;
    }
}
```

## 实际工程：配置键匹配

```cpp
#include <string_view>
#include <variant>
#include <unordered_map>

class Config {
    std::unordered_map<std::string, std::variant<int, double, std::string>> data_;

public:
    // 快速匹配已知的配置键
    std::variant<int, double, std::string>* get(std::string_view key) {
        // 对已知键用 switch，对未知键降级到 map 查找
        switch (hash(key)) {
            case hash("timeout"):   return find("timeout");
            case hash("retries"):   return find("retries");
            case hash("host"):      return find("host");
            case hash("port"):      return find("port");
            case hash("log_level"): return find("log_level");
            default:
                // 未知配置键 → 运行时查找
                auto it = data_.find(std::string(key));
                return it != data_.end() ? &it->second : nullptr;
        }
    }

private:
    std::variant<int, double, std::string>* find(const char* key) {
        auto it = data_.find(key);
        return it != data_.end() ? &it->second : nullptr;
    }
};
```

## hash 函数选择

| 算法 | 编译期友好 | 速度 | 碰撞率 | 推荐场景 |
|------|-----------|------|--------|----------|
| FNV-1a | ✅ | 快 | 低 | 短字符串，通用 |
| DJB2 | ✅ | 很快 | 中 | 对碰撞不敏感的场景 |
| xxHash | ❌ | 极快 | 极低 | 运行时长字符串 |
| CityHash | ❌ | 极快 | 极低 | 运行时长字符串 |
| CRC32 | ✅ (硬件指令) | 极快 | 高 | 校验而非哈希表 |

FNV-1a 是编译期场景的最佳选择：实现极简、无依赖、在 64 位空间下碰撞率足够低。

## 关键要点

> hash 冲突在 switch-string 中是致命的——两个不同的 case 分支会编译错误（duplicate case value）。所以必须选碰撞率低的 hash 函数，或在编译期检查碰撞。FNV-1a 64 位在几万个短字符串内几乎不会碰撞。

> `consteval` 比 `constexpr` 更安全——`constexpr` 函数可以在运行时调用（退化），`consteval` 强制只能编译期调用。这保证了 hash 值永远不会在运行时计算（除非你明确这样写）。

> switch-string 的另一种替代方案是 trie 树或完美哈希（gperf），但它们更复杂。对于 <100 个字符串的场景，FNV-1a + switch 已经足够。

## 相关模式 / 关联

- [[cpp-编译期计算与constexpr深入]] — constexpr 全面指南
- [[cpp-if-consteval]] — 编译期/运行时分支
- [[cpp-自定义字面量]] — operator"" 用法
- [[cpp-编译期校验与static_assert]] — 编译期断言
- [[cpp-string_view注意事项]] — string_view 的安全使用
