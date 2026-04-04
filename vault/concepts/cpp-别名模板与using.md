---
title: 别名模板与 using
tags: [cpp, template, alias, using, typedef, type-alias]
aliases: [别名模板, using, alias template, typedef, 类型别名]
created: 2026-04-04
updated: 2026-04-04
---

# 别名模板与 using

`using` 做类型别名——比 `typedef` 更清晰，且支持模板别名（`typedef` 不行）。

## using vs typedef

```cpp
// 两种方式等价
using StringVec = std::vector<std::string>;  // using（推荐）
typedef std::vector<std::string> StringVec;  // typedef

// using 更清晰（从左到右读）
using FuncPtr = int (*)(int, int);          // "FuncPtr 是 int(*)(int,int)"
typedef int (*FuncPtr)(int, int);           // "typedef int(*)(int,int) FuncPtr"

// using 可以用于成员类型
struct Widget {
    using value_type = int;  // typedef 不行
};
```

## 别名模板

```cpp
// 别名模板：typedef 做不到
template <typename T>
using Vec = std::vector<T, std::allocator<T>>;

Vec<int> v;                    // 等价于 std::vector<int>
Vec<std::string> strings;      // 等价于 std::vector<std::string>

// 带默认参数
template <typename K, typename V, typename Hash = std::hash<K>>
using HashMap = std::unordered_map<K, V, Hash>;

HashMap<std::string, int> scores;  // 比 std::unordered_map<std::string, int> 简洁

// 常见用法
template <typename T>
using Ptr = std::unique_ptr<T>;

template <typename T>
using Ref = std::reference_wrapper<T>;

// C++20 中 type_traits 的 _t 后缀就是别名模板
// template <typename T> using remove_const_t = typename remove_const<T>::type;
```

## 关键要点

> `using` 是 `typedef` 的完全替代——更清晰的语法，且支持模板别名。现代 C++ 统一用 `using`。

> 别名模板不能特化——需要特化时用 `struct` + `using` 组合（在 struct 中特化，外部用 using 引入）。

## 相关模式 / 关联

- [[cpp-模板编程基础]] — 模板基础
- [[cpp-type-traits]] — type_traits 中的 _t 别名
