---
title: C++ std::reference_wrapper
tags: [cpp, reference_wrapper, std::ref, container-of-references, copyable-reference]
aliases: [reference_wrapper, std::ref, 可拷贝引用, 容器中的引用]
created: 2026-04-04
updated: 2026-04-04
---

# std::reference_wrapper

`reference_wrapper` 是可拷贝、可赋值的引用包装——让引用能存在容器中或传递给需要拷贝的接口。

## 问题：引用不可拷贝

```cpp
// ❌ 引用不可重新绑定、不可拷贝
// std::vector<int&> v;  // 编译错误：引用不是类型
// std::function<void(int&)> 不能用 bind 拷贝
```

## reference_wrapper 解决

```cpp
#include <functional>

int x = 42, y = 100;
std::reference_wrapper<int> ref = std::ref(x);  // 包装引用
ref.get() = 50;  // 修改 x
ref = std::ref(y);  // 重新绑定到 y

// 存入容器
std::vector<std::reference_wrapper<int>> refs;
refs.push_back(std::ref(x));
refs.push_back(std::ref(y));
refs[0].get() = 999;  // 修改 x

// 传给需要值语义的接口
std::vector<int> data = {1, 2, 3};
std::function<void(int&)> func = [](int& n) { n *= 2; };
// 用 std::ref 传递引用
std::for_each(data.begin(), data.end(), std::ref(func));  // 不复制 func

// 传给 thread（避免拷贝）
int counter = 0;
std::thread t([&counter] { counter++; });  // 用捕获
std::thread t2(std::ref(counter));          // 用 std::ref（如果函数接受引用）
```

## 关键要点

> `std::ref(x)` 返回 `reference_wrapper<int>`——行为像引用但可拷贝、可赋值。

> `reference_wrapper` 自动隐式转换为 `T&`——大部分场景可以透明使用。

## 相关模式 / 关联

- [[cpp-引用与指针]] — 引用基础
- [[cpp-函数对象]] — 函数对象的引用传递
