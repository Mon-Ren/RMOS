---
title: 函数指针与 std::function
tags: [cpp, function-pointer, std::function, callable, type-erasure]
aliases: [函数指针, std::function, 可调用对象, callback, 类型擦除调用]
created: 2026-04-04
updated: 2026-04-04
---

# 函数指针与 std::function

函数指针是 C 遗留的调用机制，`std::function` 是类型擦除的可调用对象包装——后者可以存储函数指针、lambda、函数对象、bind 表达式。

## 函数指针

```cpp
// 函数指针类型
int add(int a, int b) { return a + b; }

// 声明
int (*fp)(int, int) = &add;   // fp 指向 add
int (*fp2)(int, int) = add;   // & 可省略

// 调用
int r = fp(1, 2);              // 3
int r2 = (*fp)(1, 2);         // 3（* 可省略）

// 函数指针类型别名
using MathFunc = int (*)(int, int);
typedef int (*MathFunc2)(int, int);  // C 风格

// 回调模式
void sort(int* arr, size_t n, int (*cmp)(int, int)) {
    // 用 cmp 比较元素
}
sort(arr, n, [](int a, int b) { return a - b; });  // lambda 隐式转换为函数指针
```

## std::function

```cpp
#include <functional>

// 存储任何可调用对象
std::function<int(int, int)> op;

op = add;                                    // 函数指针
op = [](int a, int b) { return a * b; };     // lambda
op = std::bind(std::plus<>(), std::placeholders::_1, std::placeholders::_2);  // bind

// 调用
int r = op(3, 4);  // 12

// 检查是否为空
if (op) { op(1, 2); }
if (!op) { /* 空 */ }
```

## 性能对比

```
方式              调用开销          存储开销        可存储内容
函数指针          一次间接跳转      1个指针(8字节)  仅函数指针
lambda(auto)      零开销(内联)      因捕获而异      仅该lambda
std::function     二次间接跳转+     堆分配可能       任何可调用对象
                  类型擦除开销      ~32字节
```

## 关键要点

> `std::function` 有类型擦除开销（虚函数调用 + 可能的堆分配）。如果类型已知，用 `auto` 存储 lambda 更高效。

> Lambda 可以隐式转换为函数指针（如果无捕获）。有捕获的 lambda 必须用 `std::function` 或模板参数存储。

## 相关模式 / 关联

- [[cpp-lambda表达式]] — lambda 是现代 C++ 的首选可调用对象
- [[cpp-类型擦除]] — std::function 的实现原理
