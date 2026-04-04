---
title: 枚举类型
tags: [cpp, fundamentals, enum, enum-class, scoped-enum]
aliases: [枚举, enum class, 限定作用域枚举, 枚举类]
created: 2026-04-04
updated: 2026-04-04
---

# 枚举类型

`enum class` 是现代 C++ 枚举的标准选择——强类型、有作用域、不隐式转换到整数。

## 意图与场景

- 表示有限集合的状态或选项
- 替代魔法数字，提高可读性
- 类型安全地表示互斥的选项

## 旧式 enum vs enum class

```cpp
// 旧式 enum（C 风格）——不推荐
enum Color { Red, Green, Blue };
Color c = Red;
int i = c;           // 隐式转换为 int，危险
// Red = 0;          // Red 污染外层命名空间

// enum class（C++11）——推荐
enum class Color { Red, Green, Blue };
Color c = Color::Red;   // 必须带作用域
// int i = c;           // 编译错误：不隐式转换
int i = static_cast<int>(c);  // 必须显式转换

// enum class 可以指定底层类型
enum class Color : uint8_t { Red = 0, Green = 1, Blue = 2 };
// 底层类型为 uint8_t，节省空间
```

## 枚举与 switch

```cpp
enum class Direction { Up, Down, Left, Right };

std::string to_string(Direction d) {
    switch (d) {
        case Direction::Up:    return "Up";
        case Direction::Down:  return "Down";
        case Direction::Left:  return "Left";
        case Direction::Right: return "Right";
    }
    // 如果不覆盖所有情况，且没有 default，
    // 编译器可能警告（但不会报错）
    return "Unknown";
}
```

## 位标志枚举

```cpp
enum class FileFlags : uint8_t {
    None    = 0,
    Read    = 1 << 0,  // 0b0001
    Write   = 1 << 1,  // 0b0010
    Execute = 1 << 2,  // 0b0100
};

// 使用位运算组合
constexpr FileFlags operator|(FileFlags a, FileFlags b) {
    return static_cast<FileFlags>(
        static_cast<uint8_t>(a) | static_cast<uint8_t>(b));
}

constexpr bool operator&(FileFlags a, FileFlags b) {
    return (static_cast<uint8_t>(a) & static_cast<uint8_t>(b)) != 0;
}

auto perms = FileFlags::Read | FileFlags::Write;
if (perms & FileFlags::Read) { /* 有读权限 */ }
```

## 关键要点

> 优先使用 `enum class` 而非旧式 `enum`——它提供作用域隔离和类型安全，避免了隐式转换和命名空间污染。

> 需要与 C 互操作或需要自动递增的整数常量时，可以考虑旧式 `enum`（但最好还是用 `enum class`）。

## 相关模式 / 关联

- [[cpp-基本数据类型]] — enum 的底层类型
- [[cpp-运算符重载]] — 位标志枚举的运算符重载
