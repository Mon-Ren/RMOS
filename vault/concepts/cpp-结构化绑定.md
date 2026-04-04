---
title: 结构化绑定
tags: [cpp17, structured-bindings, decomposition, tuple]
aliases: [结构化绑定, 解构, tuple解包, structured binding]
created: 2026-04-04
updated: 2026-04-04
---

# 结构化绑定（C++17）

结构化绑定让从复合类型中提取成员变得像 Python 解包一样简洁——但它是编译期机制，零运行时开销。

## 意图与场景

- 从函数返回多个值时直接解包
- 遍历 map 时直接获取 key 和 value
- 解构 struct 成员到独立变量

## 基本用法

```cpp
#include <tuple>
#include <map>

// 从 tuple 解包
std::tuple<int, double, std::string> getData() {
    return {42, 3.14, "hello"};
}
auto [id, score, name] = getData();
// id 是 int，score 是 double，name 是 string

// 从 pair 解包（常见于 map 遍历）
std::map<std::string, int> scores = {{"Alice", 95}, {"Bob", 87}};
for (const auto& [name, score] : scores) {
    std::cout << name << ": " << score << "\n";
}

// 从数组解包
int arr[3] = {1, 2, 3};
auto [a, b, c] = arr;  // a=1, b=2, c=3

// 从结构体解包
struct Point { double x, y; };
Point p{1.0, 2.0};
auto [x, y] = p;  // x=1.0, y=2.0
```

## 引用绑定

```cpp
// 修改原始数据
std::tuple<int, int> coords{10, 20};
auto& [cx, cy] = coords;
cx = 100;  // coords 变为 {100, 20}

// const 引用
const auto& [k, v] = *scores.begin();

// 移动语义
auto&& [val] = std::make_tuple(42);  // val 是右值引用
```

## 实际应用

```cpp
// 多返回值的优雅处理
auto [success, result, error] = tryParse(input);
if (!success) {
    log(error);
    return;
}
use(result);

// map 的 insert 返回 pair
auto [it, inserted] = myMap.insert({key, value});
if (!inserted) {
    // key 已存在
}

// 用于锁
std::mutex mtx;
std::map<int, std::string> data;
// 需要同时持有锁和迭代器
auto locked = std::pair<std::unique_lock<std::mutex>, std::string*>{...};
```

## 底层机制

```cpp
// 结构化绑定不是引用的语法糖，而是创建了绑定到成员的别名
// 对于 struct：绑定到每个 public 成员（按声明顺序）
// 对于 tuple/pair：绑定到 get<0>(), get<1>(), ...
// 对于数组：绑定到每个元素

// 注意：不能只绑定部分成员
// auto [first, , third] = tuple;  // C++ 不支持
```

## 关键要点

> 结构化绑定是编译期机制，没有运行时开销。绑定的名字是原始对象成员的别名，不是拷贝（除非用了 `auto` 且原始对象是值）。

> 结构化绑定的变量数量必须与成员数量严格匹配——不能跳过、不能部分绑定。

## 相关模式 / 关联

- [[cpp-auto-与类型推导]] — auto 在结构化绑定中的行为
- [[cpp-lambda表达式]] — C++20 中 lambda 参数的结构化绑定
