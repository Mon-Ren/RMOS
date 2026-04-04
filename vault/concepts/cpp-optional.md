---
title: std::optional（C++17）
tags: [cpp17, optional, nullable, maybe, monadic]
aliases: [optional, 可选值, 空值安全, monadic]
created: 2026-04-04
updated: 2026-04-04
---

# std::optional（C++17）

`optional` 是类型安全的"可能有值，可能无值"——终结了返回指针/特殊值来表示"无结果"的陋习。

## 意图与场景

- 函数可能不返回结果（查找失败、解析失败）
- 替代 `nullptr` / `-1` / `""` 作为"无值"标记
- 延迟初始化

## 基本用法

```cpp
#include <optional>
#include <string>

std::optional<std::string> find_user(int id) {
    if (auto it = db.find(id); it != db.end())
        return it->second.name;   // 有值
    return std::nullopt;          // 无值
}

// 使用
auto name = find_user(42);
if (name) {                            // 检查是否有值
    std::cout << *name << "\n";        // 解引用获取值
}
std::cout << name.value_or("Unknown"); // 无值时返回默认值

// 检查
name.has_value();    // bool
name.value();        // 有值返回值，无值抛 std::bad_optional_access
name.value_or("N/A"); // 无值返回参数值
```

## C++23 单子操作

```cpp
// transform：有值时映射，无值时透传 nullopt
std::optional<int> len = find_user(42).transform([](const auto& s) {
    return s.size();
});

// and_then：链式调用可能失败的操作
std::optional<int> parse(const std::string& s);
std::optional<int> double_if_positive(int n);

auto result = parse("42")
    .and_then(double_if_positive)    // 返回 optional<int>
    .transform([](int n) { return n * 2; });  // 返回 optional<int>
// 整个链中任一步返回 nullopt 则最终结果 nullopt
```

## 与指针的对比

```cpp
// ❌ 用指针表示可选值
std::string* find_name(int id);  // 返回 nullptr？悬垂指针？谁拥有内存？

// ✅ 用 optional
std::optional<std::string> find_name(int id);  // 值语义，无所有权问题
```

## 关键要点

> `optional` 是值语义的"可能为空"——它拥有内部的值，不会悬垂。比返回指针或特殊值安全得多。

> `optional<T&>` 在 C++ 中不存在（标准不允许），需要引用时用 `std::reference_wrapper<T>`。

## 相关模式 / 关联

- [[cpp-variant]] — 类型安全的联合体
- [[cpp-expected]] — C++23 的值或错误
