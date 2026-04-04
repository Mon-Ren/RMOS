---
title: C++ 编译期分支与 if constexpr 最佳实践
tags: [cpp17, if-constexpr, best-practices, template, static-assert]
aliases: [if constexpr最佳实践, 编译期分支模式, constexpr if patterns]
created: 2026-04-04
updated: 2026-04-04
---

# if constexpr 最佳实践

`if constexpr` 的正确使用模式——以及常见陷阱。

## 正确用法

```cpp
// 模式 1：类型特征分支
template <typename T>
auto to_number(const T& val) {
    if constexpr (std::is_arithmetic_v<T>) {
        return static_cast<double>(val);
    } else if constexpr (std::is_same_v<T, std::string>) {
        return std::stod(val);
    } else {
        static_assert(sizeof(T) == 0, "Unsupported type");
    }
}

// 模式 2：检查成员存在
template <typename T>
auto get_size(const T& container) {
    if constexpr (requires { container.size(); }) {
        return container.size();
    } else {
        return std::distance(container.begin(), container.end());
    }
}

// 模式 3：容器 vs 非容器
template <typename T>
void print(const T& val) {
    if constexpr (std::ranges::range<T>) {
        for (const auto& elem : val) print(elem);
    } else {
        std::cout << val << "\n";
    }
}
```

## 常见陷阱

```cpp
// ❌ 陷阱 1：条件不是编译期常量
int x = 42;
// if constexpr (x > 0) { }  // 编译错误：x 不是常量表达式

// ✅ 修复
constexpr int y = 42;
if constexpr (y > 0) { }

// ❌ 陷阱 2：return 在 if constexpr 分支中
template <typename T>
int process(T val) {
    if constexpr (std::is_integral_v<T>) {
        return val * 2;  // OK
    }
    // ⚠️ 如果 T 不是整数类型，编译器看到没有 return
    // 某些编译器会警告"没有 return"
    return 0;  // ✅ 加兜底 return
}

// ❌ 陷阱 3：else 分支中仍有语法错误
template <typename T>
void bad(T val) {
    if constexpr (std::is_integral_v<T>) {
        // ...
    } else {
        val.nonexistent_method();  // 如果其他分支没有 return，这段仍需编译
    }
}
```

## 关键要点

> `if constexpr` 的不满足分支在模板实例化时不编译——但如果函数需要返回值，确保所有路径都有 return。

> 配合 `requires` 表达式（C++20）使用效果最佳——检测类型能力而非类型身份。

## 相关模式 / 关联

- [[cpp-if-constexpr]] — if constexpr 基础
- [[cpp-concepts]] — C++20 约束
