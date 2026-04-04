---
title: 函数对象（Functor）
tags: [cpp, functor, function-object, operator, stateful]
aliases: [函数对象, functor, 仿函数, operator(), 带状态函数]
created: 2026-04-04
updated: 2026-04-04
---

# 函数对象（Functor）

函数对象是重载了 `operator()` 的类——在 Lambda 之前是 STL 算法的主要回调方式，现在仍用于需要状态或模板的场景。

## 基本形式

```cpp
// 函数对象：有状态的"函数"
struct Counter {
    int count = 0;
    void operator()(int x) {
        ++count;
        std::cout << x << "\n";
    }
};

Counter c;
c(1);  // count = 1
c(2);  // count = 2
std::cout << "Count: " << c.count << "\n";

// 用于算法
std::vector<int> v = {1, 2, 3, 4, 5};
Counter counter;
std::for_each(v.begin(), v.end(), counter);
// counter.count 仍为 0！按值传递，修改的是副本
// 用 std::ref 包装：
std::for_each(v.begin(), v.end(), std::ref(counter));
// counter.count == 5
```

## 预定义函数对象

```cpp
#include <functional>

std::plus<>{}(1, 2);          // 3
std::minus<>{}(5, 3);         // 2
std::multiplies<>{}(2, 3);    // 6
std::divides<>{}(6, 2);       // 3
std::modulus<>{}(7, 3);       // 1
std::negate<>{}(5);           // -5

std::equal_to<>{}(1, 1);      // true
std::not_equal_to<>{}(1, 2);  // true
std::less<>{}(1, 2);          // true
std::greater<>{}(2, 1);       // true

std::logical_and<>{}(true, false);   // false
std::logical_or<>{}(true, false);    // true
std::logical_not<>{}(true);          // false

// 用于容器排序
std::set<int, std::greater<int>> desc_set;
std::priority_queue<int, std::vector<int>, std::greater<int>> min_heap;
```

## Lambda vs 函数对象

```
场景                                选择
────────────────────────────────────────────
简单一次性回调                      Lambda
需要保持状态                        Lambda（捕获变量）或 函数对象
需要模板 operator()                 函数对象或 泛型 Lambda（C++14）
需要多态接口                        函数对象（继承基类）
性能敏感（需内联）                  Lambda 或 函数对象
```

## 关键要点

> Lambda 本质上是编译器生成的函数对象——`[](int x){ return x*x; }` 产生一个匿名类。两者在性能上无差异。

> `std::greater<>`（C++14 起的透明版本）比 `std::greater<int>` 更灵活——不需要指定类型，支持异构比较。

## 相关模式 / 关联

- [[cpp-lambda表达式]] — Lambda 是函数对象的语法糖
- [[cpp-stl算法总览]] — 算法中使用函数对象
