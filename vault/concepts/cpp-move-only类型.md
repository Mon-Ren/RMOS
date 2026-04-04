---
title: Move-only 类型
tags: [cpp, move-only, unique-ownership, non-copyable, movable]
aliases: [move-only, 不可拷贝, 独占所有权, non-copyable, 只可移动]
created: 2026-04-04
updated: 2026-04-04
---

# Move-only 类型

Move-only 类型只能移动不能拷贝——表达"独占所有权"的语义，`unique_ptr`、`thread`、`fstream` 都是典型代表。

## 设计 Move-only 类型

```cpp
class UniqueResource {
    int* data_;
public:
    explicit UniqueResource(int val) : data_(new int(val)) {}

    // 析构
    ~UniqueResource() { delete data_; }

    // 禁止拷贝
    UniqueResource(const UniqueResource&) = delete;
    UniqueResource& operator=(const UniqueResource&) = delete;

    // 允许移动
    UniqueResource(UniqueResource&& other) noexcept : data_(other.data_) {
        other.data_ = nullptr;
    }

    UniqueResource& operator=(UniqueResource&& other) noexcept {
        if (this != &other) {
            delete data_;
            data_ = other.data_;
            other.data_ = nullptr;
        }
        return *this;
    }
};
```

## 使用场景

```cpp
// std::unique_ptr 是最常用的 move-only 类型
auto p = std::make_unique<Widget>();
auto q = std::move(p);   // p 变为 null

// std::thread 是 move-only
std::thread t1(work);
std::thread t2 = std::move(t1);  // t1 变为空
// std::thread t3 = t1;  // 编译错误：不可拷贝

// std::fstream 是 move-only
std::ifstream file("data.txt");
std::ifstream file2 = std::move(file);  // 转移文件所有权
```

## 在容器中使用

```cpp
// vector 可以存储 move-only 类型
std::vector<std::unique_ptr<Widget>> widgets;
widgets.push_back(std::make_unique<Widget>());
widgets.push_back(std::move(another_ptr));

// push_back 触发移动构造（unique_ptr 支持）

// map 中存储 move-only 值
std::map<int, std::unique_ptr<Widget>> registry;
registry[1] = std::make_unique<Widget>();  // OK：move assignment

// ⚠️ 不能用 initializer_list 初始化 move-only 类型
// std::vector<std::unique_ptr<int>> v = {
//     std::make_unique<int>(1),  // 编译错误！initializer_list 拷贝元素
//     std::make_unique<int>(2)
// };
```

## 关键要点

> Move-only 类型通过 `= delete` 禁止拷贝构造和拷贝赋值。移动后源对象处于 valid-but-unspecified 状态，可以安全地赋新值或析构。

> initializer_list 要求元素可拷贝——move-only 类型不能用 initializer_list 初始化，用 push_back/emplace_back 替代。

## 相关模式 / 关联

- [[cpp-右值引用与移动语义]] — 移动语义基础
- [[cpp-Rule-of-Zero与Rule-of-Five]] — 特殊成员函数管理
