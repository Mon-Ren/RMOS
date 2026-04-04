---
title: const 正确性
tags: [cpp, const-correctness, const, immutable, design]
aliases: [const正确性, 常量正确, const correctness, 不可变设计]
created: 2026-04-04
updated: 2026-04-04
---

# const 正确性

const 正确性是一种设计原则——尽可能让数据不可变，让编译器帮你捕获"不该修改却被修改"的 bug。

## 从右往左读规则

```cpp
const int* p1;          // pointer to const int（指针指向的内容不可变）
int const* p2;          // 同上
int* const p3;          // const pointer to int（指针本身不可变）
const int* const p4;    // const pointer to const int

// 从右往左读：
// p1 → * → const int → "指向 const int 的指针"
// p3 → const → * → int → "const 指针，指向 int"
```

## const 成员函数

```cpp
class Text {
    std::string content_;
    mutable size_t hash_cache_;   // mutable：const 函数中可修改
public:
    // const 成员函数：承诺不修改逻辑状态
    size_t length() const { return content_.size(); }

    // const 重载：const 对象调用 const 版本
    char operator[](size_t i) const { return content_[i]; }
    char& operator[](size_t i) { return content_[i]; }

    // mutable：缓存计算结果（逻辑上是 const，物理上需要写）
    size_t hash() const {
        if (hash_cache_ == 0) {
            hash_cache_ = compute_hash(content_);
        }
        return hash_cache_;
    }
};

const Text t = get_text();
t.length();          // OK：const 函数
// t[0] = 'A';       // 编译错误：const 对象调用 const[]
```

## const 引用参数

```cpp
// 规则：
// 不修改 → const T&（避免拷贝）
// 需要修改 → T&
// 转移所有权 → T&&
// 基本类型（int, double）→ 按值传递

void print(const std::string& s);    // 不修改，不拷贝
void transform(std::string& s);      // 需要修改
void take(std::string s);            // 按值，可以移动（适合小类型）
```

## const 迭代器

```cpp
std::vector<int> v = {1, 2, 3};

// const_iterator：不能修改指向的元素
std::vector<int>::const_iterator it = v.cbegin();
// *it = 42;  // 编译错误

// const 对象只能获取 const_iterator
const std::vector<int>& cv = v;
auto cit = cv.begin();  // const_iterator

// C++11: cbegin/cend 返回 const_iterator
auto it2 = v.cbegin();  // const_iterator（即使 v 非 const）
```

## 关键要点

> const 正确性从内到外：先让函数参数和成员函数 const，再让变量和返回值 const。不能反过来。

> `mutable` 不是 const 的"后门"——它用于缓存、调试计数等不影响逻辑状态的物理修改。

## 相关模式 / 关联

- [[cpp-const与constexpr]] — constexpr 是更强的 const
- [[cpp-类与对象]] — const 成员函数
