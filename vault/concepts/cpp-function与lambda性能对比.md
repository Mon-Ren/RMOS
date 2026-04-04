---
title: C++ std::function 与 Lambda 性能对比
tags: [cpp, function, lambda, performance, type-erasure, inline]
aliases: [function性能, lambda性能, 类型擦除开销, 虚调用开销]
created: 2026-04-04
updated: 2026-04-04
---

# std::function 与 Lambda 性能对比

`std::function` 和 Lambda 在性能上有本质差异——类型已知时用 Lambda，类型擦除时用 function。

## 性能差异

```cpp
// Lambda + auto：零开销（编译器知道具体类型）
auto lambda = [](int x) { return x * x; };
auto result = lambda(5);  // 内联展开，无函数调用

// std::function：类型擦除开销
std::function<int(int)> func = [](int x) { return x * x; };
auto result2 = func(5);   // 虚函数调用 + 可能的堆分配
```

## 基准测试

```
方式                 调用耗时      内存     可内联
auto lambda          ~0ns         因捕获    是
函数指针             ~1ns         8字节    否（除非确定）
std::function        ~5-10ns      32字节   否
std::function(SBO)   ~3-5ns       32字节   否
```

## 何时用哪个

```cpp
// 用 auto lambda：类型已知，性能关键
auto callback = [&data](int x) { return data.process(x); };
std::sort(v.begin(), v.end(), [](int a, int b) { return a > b; });

// 用 std::function：类型需要存储、传递、异构
std::map<int, std::function<int(int)>> handlers;
handlers[1] = [](int x) { return x * 2; };
handlers[2] = [](int x) { return x + 1; };

// 用函数指针：与 C 互操作、回调接口
using Callback = void(*)(int);
void register_callback(Callback cb);
```

## 关键要点

> `auto` 存储的 Lambda 零开销——编译器可以内联展开。`std::function` 有类型擦除开销——虚调用 + 可能的堆分配。

> 性能关键路径上避免 `std::function`——用模板参数或 `auto` 保持类型信息。

## 相关模式 / 关联

- [[cpp-function实现原理]] — function 的内部实现
- [[cpp-函数指针与function]] — function 的使用
