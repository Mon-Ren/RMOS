---
title: C++20 主要特性汇总
tags: [cpp20, features, concepts, ranges, coroutines, modules, spaceship]
aliases: [C++20, 特性汇总, concepts, ranges, 协程, modules]
created: 2026-04-04
updated: 2026-04-04
---

# C++20 主要特性汇总

C++20 是继 C++11 以来最大的更新——四个大特性加上大量实用改进。

## 四大特性

```cpp
// 1. Concepts：模板约束
template <typename T> requires std::integral<T>
T gcd(T a, T b);

// 2. Ranges：管道式数据处理
auto result = nums | rv::filter(is_even) | rv::transform(square) | rv::take(5);

// 3. 协程：co_await/co_yield/co_return
std::generator<int> range(int n) {
    for (int i = 0; i < n; ++i) co_yield i;
}

// 4. Modules：替代头文件
import std;  // C++23，替代 #include
import math;
```

## 语言特性

```cpp
// Spaceship 运算符 <=>
auto operator<=>(const Point&) const = default;

// consteval：强制编译期
consteval int must_compile_time(int n) { return n * n; }

// constinit：编译期初始化
constinit int global = 42;

// Lambda 模板
auto f = []<typename T>(T val) { return sizeof(T); };

// using enum
enum class Color { Red, Green, Blue };
using enum Color;  // 引入所有枚举值
auto c = Red;      // 不需要 Color::Red

// 聚合初始化改进
struct Base { int x; };
struct Derived : Base { int y; };
Derived d{{1}, 2};  // C++20 聚合初始化带基类

// 指定初始化
struct Point { double x, y, z; };
Point p{.x = 1.0, .z = 3.0};  // .y 默认初始化

// 范围 for 中的初始化语句
for (auto vec = get_data(); auto& item : vec) { }

// [[likely]], [[unlikely]], [[no_unique_address]] 属性

// char8_t 类型（UTF-8）
char8_t c = u8'A';
```

## 库特性

```cpp
// std::format
std::string s = std::format("Hello, {}!", name);

// std::span
void process(std::span<const int> data);

// std::jthread（自动 join + 停止令牌）
std::jthread t([](std::stop_token st) {
    while (!st.stop_requested()) work();
});

// std::counting_semaphore, std::latch, std::barrier

// std::endian
constexpr bool little = std::endian::native == std::endian::little;

// std::to_array
auto arr = std::to_array<int>({1, 2, 3});

// std::bind_front
auto add5 = std::bind_front(std::plus<>{}, 5);

// std::bit_cast
uint32_t bits = std::bit_cast<uint32_t>(3.14f);
```

## 关键要点

> C++20 的 Concepts 和 Ranges 改变了写泛型代码的方式。协程提供了异步编程的新范式。Modules 还在成熟中。

> `import std;`（C++23）是 modules 的里程碑——标准库的模块化导入，大幅加速编译。

## 相关模式 / 关联

- [[cpp-concepts]] — Concepts 专题
- [[cpp-range库]] — Ranges 专题
- [[cpp-协程]] — 协程专题
