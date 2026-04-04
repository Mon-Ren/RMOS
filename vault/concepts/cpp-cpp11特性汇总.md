---
title: C++11 主要特性汇总
tags: [cpp11, features, auto, lambda, move, smart-pointer, range-for]
aliases: [C++11, 特性汇总, auto, lambda, 移动语义, 智能指针]
created: 2026-04-04
updated: 2026-04-04
---

# C++11 主要特性汇总

C++11 是 C++ 的"文艺复兴"——现代 C++ 从这里开始。

## 语言特性

```cpp
// auto 类型推导
auto x = 42;                    // int
auto it = vec.begin();          // 迭代器类型

// range-based for
for (const auto& item : vec) { std::cout << item; }

// lambda 表达式
auto add = [](int a, int b) { return a + b; };

// 右值引用与移动语义
Widget(Widget&& other) noexcept;
std::move(x);

// 完美转发
template <typename T> void f(T&& arg) { g(std::forward<T>(arg)); }

// enum class
enum class Color { Red, Green, Blue };

// nullptr（替代 NULL）
int* p = nullptr;

// static_assert
static_assert(sizeof(int) == 4, "");

// 委托构造函数
Widget() : Widget(0, "") {}
Widget(int x, const std::string& s);

// override 和 final
void foo() override;
void bar() final;

// 强类型枚举、统一初始化、列表初始化
std::vector<int> v = {1, 2, 3};
Widget w{42, "hello"};

// constexpr
constexpr int square(int x) { return x * x; }

// 变长模板
template <typename... Args> void print(Args... args);

// 原始字符串
auto path = R"(C:\Users\file.txt)";

// 用户定义字面量
auto time = 30s;

// defaulted / deleted 函数
Widget() = default;
Widget(const Widget&) = delete;
```

## 库特性

```cpp
// 智能指针
auto p = std::make_shared<Widget>();
auto q = std::make_unique<Widget>();  // C++14，但基于 C++11

// 线程
std::thread t(work);
std::mutex mtx;
std::lock_guard<std::mutex> lock(mtx);
std::condition_variable cv;
std::future<int> f = std::async(compute, 42);

// 容器
std::array<int, 10> a;
std::unordered_map<std::string, int> um;
std::forward_list<int> fl;

// 其他
std::tuple<int, double, std::string> t;
std::function<int(int)> fn;
std::bind(&Foo::bar, &obj, std::placeholders::_1);
std::chrono::high_resolution_clock::now();
std::regex pattern(R"(\d+)");
std::atomic<int> counter{0};
```

## 关键要点

> C++11 的五大改变：auto、lambda、移动语义、智能指针、线程库。它们重新定义了 C++ 的编程风格。

## 相关模式 / 关联

- [[cpp-auto与类型推导]] — auto 专题
- [[cpp-lambda表达式]] — lambda 专题
- [[cpp-右值引用与移动语义]] — 移动语义专题
