---
title: if constexpr（C++17）
tags: [cpp17, if-constexpr, compile-time, branch, template]
aliases: [if constexpr, 编译期分支, constexpr if]
created: 2026-04-04
updated: 2026-04-04
---

# if constexpr（C++17）

`if constexpr` 在编译期丢弃不满足条件的分支——不实例化的分支即使语法有错也不报错，彻底替代了 SFINAE 和标签分发的部分场景。

## 意图与场景

- 模板中根据类型特征选择不同实现
- 替代 `enable_if` 和标签分发的繁琐写法
- 编译期消除不需要的代码分支

## 基本用法

```cpp
template <typename T>
auto get_value(const T& t) {
    if constexpr (std::is_pointer_v<T>) {
        return *t;              // T 是指针时才编译这段
    } else {
        return t;               // T 不是指针时才编译这段
    }
}

int x = 42;
get_value(&x);   // 编译 *t 分支
get_value(x);    // 编译 t 分支
// 注意：对于 int 类型，*t 不会编译（即使写在源码中）
```

## 实际应用

```cpp
// 不同类型不同的序列化方式
template <typename T>
std::string serialize(const T& val) {
    if constexpr (std::is_arithmetic_v<T>) {
        return std::to_string(val);
    } else if constexpr (std::is_same_v<T, std::string>) {
        return "\"" + val + "\"";
    } else if constexpr (std::is_same_v<T, bool>) {
        return val ? "true" : "false";
    } else {
        static_assert(sizeof(T) == 0, "Unsupported type");  // 编译时就报错
    }
}

// 简化 SFINAE
template <typename Container>
auto size_or_zero(const Container& c) {
    if constexpr (requires { c.size(); }) {  // C++20: requires 表达式
        return c.size();
    } else {
        return 0;
    }
}
```

## if constexpr vs 普通 if

```cpp
// 普通 if：两个分支都必须语法正确
template <typename T>
void bad_example(T t) {
    if (std::is_pointer_v<T>) {
        std::cout << *t;      // 对于非指针 T，即使不执行这段也必须语法正确
    }
}
// bad_example(42);  // 编译错误：int 不支持 * 操作

// if constexpr：不满足的分支不实例化
template <typename T>
void good_example(T t) {
    if constexpr (std::is_pointer_v<T>) {
        std::cout << *t;      // 对于非指针 T，这段不编译
    }
}
// good_example(42);  // OK
```

## 关键要点

> `if constexpr` 的分支在编译期选择——不满足的分支不会被实例化。这是它与普通 `if` 的根本区别。

> `if constexpr` 不能用于运行时条件——条件必须是编译期可求值的常量表达式。

## 相关模式 / 关联

- [[cpp-sfinae-与编译期多态]] — if constexpr 替代了部分 SFINAE
- [[cpp-标签分发]] — if constexpr 替代了部分标签分发
