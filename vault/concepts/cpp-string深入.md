---
title: std::string 深入
tags: [cpp, stl, string, text, encoding]
aliases: [string, 字符串, string_view, SSO, 短字符串优化]
created: 2026-04-04
updated: 2026-04-04
---

# std::string 深入

`std::string` 是 C++ 的字符串主力——SSO（短字符串优化）让它在大多数场景下性能优秀，但理解它的拷贝语义和内存管理才能用好它。

## 意图与场景

- 动态长度字符串操作
- 不需要手动管理内存的字符串容器
- 与 C 字符串互操作

## SSO（短字符串优化）

```
大多数实现对短字符串（通常 ≤ 15 或 22 字节）不堆分配：

长字符串布局：          短字符串布局（SSO）：
┌─────────────┐         ┌─────────────┐
│ ptr ──→ 堆  │         │ buf[16]     │  ← 数据存在对象内部
│ size        │         │ size        │
│ capacity    │         │ capacity    │
└─────────────┘         └─────────────┘

SSO 消除了短字符串的堆分配，这是 std::string 在实践中快的重要原因。
```

## 常用操作

```cpp
std::string s = "hello";

// 修改
s += " world";                    // 追加
s.append("!!!");                  // 追加
s.insert(5, ",");                 // 在位置 5 插入
s.erase(5, 1);                    // 从位置 5 删 1 个
s.replace(0, 5, "Hello");         // 替换
s.clear();                        // 清空内容（capacity 不变）

// 查询
s.find("lo");                     // 返回位置或 npos
s.find_first_of("aeiou");        // 找第一个元音
s.substr(0, 5);                   // 子串
s.starts_with("hel");            // C++20
s.ends_with("rld");              // C++20

// 转换
int n = std::stoi("42");          // string → int
double d = std::stod("3.14");     // string → double
std::string num = std::to_string(42);  // int → string

// C 互操作
const char* cstr = s.c_str();     // 返回 null 结尾的 C 字符串
const char* data = s.data();      // C++11 保证返回 null 结尾
```

## string_view（C++17）

```cpp
#include <string_view>

// string_view：非拥有引用，零拷贝
void process(std::string_view sv) {  // 接受 string、字面量、char* 都行
    std::cout << sv << "\n";
}

process("hello");                // 零拷贝
process(std::string("world"));   // 零拷贝
process(existing_string);        // 零拷贝

// ⚠️ string_view 不拥有数据——指向的字符串必须存活
std::string_view dangling() {
    std::string s = "oops";
    return s;  // 悬垂引用！s 已销毁
}
```

## 关键要点

> `string_view` 是函数参数的默认选择（代替 `const std::string&`），因为它接受任何字符串类型而零拷贝。但绝不返回局部 string 的 `string_view`。

> SSO 使得短字符串几乎零开销——`sizeof(std::string)` 通常 32 字节，但大多数短字符串不需要堆分配。

## 相关模式 / 关联

- [[cpp-右值引用与移动语义]] — string 的移动语义
- [[cpp-const与constexpr]] — constexpr string（C++20）
