---
title: auto 与类型推导
tags: [cpp, fundamentals, auto, type-deduction, decltype]
aliases: [auto关键字, 类型推导, decltype, 尾置返回类型]
created: 2026-04-04
updated: 2026-04-04
---

# auto 与类型推导

`auto` 不是动态类型——它让编译器替你写类型名，推导发生在编译期，类型在编译时就完全确定了。

## 意图与场景

- 减少冗长的类型声明，尤其是迭代器和模板
- 避免隐式窄化转换导致的意外
- 与泛型代码配合，写出更通用的函数

## auto 推导规则

`auto` 的推导规则本质上与模板参数推导一致：

```cpp
// 规则 1：值语义——剥掉引用和 cv 限定符
int x = 42;
const int& rx = x;
auto a = rx;        // a 是 int（去掉了 const 和 &）

// 规则 2：引用语义——保留引用
auto& b = rx;       // b 是 const int&

// 规则 3：const auto& —— 万能安全选项
const auto& c = rx; // c 是 const int&

// 规则 4：指针保留
int* p = &x;
auto d = p;         // d 是 int*
auto* e = p;        // e 是 int*

// 特例：initializer list
auto il = {1, 2, 3};  // il 是 std::initializer_list<int>
// auto il2 = {1, 2.0}; // 编译错误：类型不一致
```

## auto 的常见用法

```cpp
// 迭代器：不再写地狱般的类型名
std::map<std::string, std::vector<int>> data;
for (auto it = data.begin(); it != data.end(); ++it) { }

// 范围 for：更简洁
for (const auto& [key, value] : data) { }  // C++17 结构化绑定

// Lambda 表达式类型不可命名
auto lambda = [](int x) { return x * x; };

// 模板返回值
template <typename T, typename U>
auto add(T a, U b) -> decltype(a + b) {  // C++11 尾置返回类型
    return a + b;
}
// C++14 简化：
template <typename T, typename U>
auto add(T a, U b) { return a + b; }
```

## decltype：表达式类型查询

```cpp
int x = 0;
decltype(x) y = 10;          // y 是 int
decltype((x)) z = x;         // z 是 int&（注意括号！）

// decltype vs auto：
// auto：根据初始化值推导
// decltype：根据表达式确定类型（精确保留引用和 cv）

// 常见场景：声明依赖其他表达式类型的变量
std::vector<int> v;
decltype(v.size()) count = 0;  // count 的类型与 size() 返回值相同
```

## auto 的陷阱

```cpp
// 陷阱 1：auto 去掉了 const
const int cx = 42;
auto ax = cx;          // ax 是 int，不是 const int！
ax = 100;              // OK，cx 不受影响

// 陷阱 2：std::vector<bool> 的代理对象
std::vector<bool> flags = {true, false, true};
auto flag = flags[0];  // flag 不是 bool&，是代理对象的拷贝！

// 陷阱 3：不可用于函数参数（C++14 前）
// void foo(auto x) { }  // C++20 才支持

// 陷阱 4：不可用于类成员
// class Foo { auto member = 0; };  // 不允许
```

## 关键要点

> `auto` 是编译期类型推导，不产生任何运行时开销，优先用于类型冗长或显而易见的场景。

> `decltype(expr)` 精确保留表达式的类型（包括引用和 cv），而 `auto` 会剥掉它们。

## 相关模式 / 关联

- [[cpp-基本数据类型]] — auto 推导涉及的类型
- [[cpp-模板编程基础]] — 模板参数推导与 auto 推导规则一致
