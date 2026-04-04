---
title: Lambda 在 STL 算法中的应用
tags: [cpp, lambda, stl, algorithm, predicate, callback, comparator]
aliases: [lambda与算法, 谓词, predicate, callback, 算法回调]
created: 2026-04-04
updated: 2026-04-04
---

# Lambda 在 STL 算法中的应用

Lambda 是 STL 算法的灵魂——排序谓词、查找条件、变换函数都用 Lambda 表达。

## 排序

```cpp
std::vector<int> v = {3, 1, 4, 1, 5};

// 升序（默认）
std::sort(v.begin(), v.end());

// 降序
std::sort(v.begin(), v.end(), [](int a, int b) { return a > b; });

// 按成员排序
std::vector<Person> people;
std::sort(people.begin(), people.end(),
    [](const Person& a, const Person& b) { return a.age < b.age; });

// 多条件排序
std::sort(people.begin(), people.end(),
    [](const Person& a, const Person& b) {
        if (a.name != b.name) return a.name < b.name;
        return a.age < b.age;
    });

// C++20: ranges + projection
std::ranges::sort(people, {}, &Person::age);  // 按 age 排序
```

## 查找与过滤

```cpp
std::vector<int> v = {1, 2, 3, 4, 5};

// 查找第一个 > 3 的元素
auto it = std::find_if(v.begin(), v.end(), [](int x) { return x > 3; });

// 统计偶数个数
int evens = std::count_if(v.begin(), v.end(), [](int x) { return x % 2 == 0; });

// 是否所有正数
bool all_pos = std::all_of(v.begin(), v.end(), [](int x) { return x > 0; });

// 移除偶数
v.erase(
    std::remove_if(v.begin(), v.end(), [](int x) { return x % 2 == 0; }),
    v.end()
);
```

## 变换

```cpp
std::vector<int> src = {1, 2, 3, 4, 5};
std::vector<int> dst;

// 平方
std::transform(src.begin(), src.end(), std::back_inserter(dst),
    [](int x) { return x * x; });

// 过滤 + 变换（分两步）
std::vector<int> filtered;
std::copy_if(src.begin(), src.end(), std::back_inserter(filtered),
    [](int x) { return x % 2 == 0; });
std::transform(filtered.begin(), filtered.end(), filtered.begin(),
    [](int x) { return x * 10; });

// C++20: ranges 管道一步到位
auto result = src | rv::filter([](int x) { return x % 2 == 0; })
                  | rv::transform([](int x) { return x * 10; });
```

## 聚合

```cpp
std::vector<int> v = {1, 2, 3, 4, 5};

// 求和
int sum = std::accumulate(v.begin(), v.end(), 0);

// 自定义聚合（拼接字符串）
auto words = std::vector<std::string>{"hello", "world"};
std::string sentence = std::accumulate(
    words.begin(), words.end(), std::string{},
    [](const std::string& a, const std::string& b) {
        return a.empty() ? b : a + " " + b;
    });
// "hello world"
```

## 关键要点

> Lambda 让 STL 算法从"可用"变成"好用"——一行 Lambda 替代整个函数对象类。

> 捕获的 Lambda 比无捕获 Lambda 大——性能敏感时注意。简单条件可以用 `std::greater<>()` 等预定义函数对象。

## 相关模式 / 关联

- [[cpp-lambda表达式]] — Lambda 基础
- [[cpp-stl算法总览]] — STL 算法
