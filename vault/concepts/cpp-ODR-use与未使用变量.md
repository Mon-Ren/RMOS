---
title: C++ ODR-use 与未使用变量
tags: [cpp, ODR-use, unused-variable, compiler-warning, maybe_unused]
aliases: [ODR-use, 未使用变量, unused variable, 变量是否使用]
created: 2026-04-04
updated: 2026-04-04
---

# ODR-use 与未使用变量

ODR-use 决定变量是否需要定义——未使用变量会产生警告，但有几种原因你可能需要"保留"它。

## ODR-use 规则

```cpp
// 变量被 ODR-use：需要定义（需要分配存储）
int x = 42;
int* p = &x;       // ODR-use：取地址
int& r = x;        // ODR-use：绑定引用
int y = x;         // 非 ODR-use：编译期可用时可优化掉

// constexpr 变量非 ODR-use 时不需要定义
constexpr int N = 10;
int arr[N];        // 非 ODR-use：N 是编译期常量，不需要定义
// int* p = &N;     // ODR-use：需要定义 constexpr int N
```

## 处理未使用变量

```cpp
// 方法 1：[[maybe_unused]] 属性（C++17，推荐）
[[maybe_unused]] int debug_count = compute_debug_count();

// 方法 2：(void) 强制"使用"
int unused = expensive_compute();
(void)unused;

// 方法 3：编译器特定
int x = 42;
(void)x;           // C/C++ 通用
(void)sizeof(x);   // 不执行，只消除警告

// 方法 4：从设计上消除——如果不需要就不要声明
```

## 常见场景

```cpp
// 调试版本才需要的变量
#ifdef DEBUG
    [[maybe_unused]] auto start = std::chrono::steady_clock::now();
#endif
// Release 模式未使用 → maybe_unused 抑制警告

// RAII 对象只在析构时有副作用
{
    [[maybe_unused]] std::lock_guard<std::mutex> lock(mtx_);
    // lock 的作用是析构时解锁，构造后的变量本身未"使用"
}

// assert 中的变量
assert(compute_something() > 0);
// Release 模式 assert 被移除 → 变量未使用
[[maybe_unused]] int result = compute_something();
assert(result > 0);
```

## 关键要点

> `[[maybe_unused]]` 是处理"故意不使用"变量的现代方式——比 `(void)x` 更清晰。

> 未使用变量警告是真实的 bug 来源——不要全局禁用，逐个标记或修复。

## 相关模式 / 关联

- [[cpp-属性]] — C++ 标准属性
- [[cpp-编译器警告指南]] — 编译器警告
