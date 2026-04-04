---
title: C++ 表达式模板
tags: [cpp, expression-template, lazy-evaluation, Eigen, operator-overloading]
aliases: [表达式模板, expression template, 延迟求值, 矩阵库]
created: 2026-04-04
updated: 2026-04-04
---

# 表达式模板

表达式模板让 `a + b + c` 不创建中间对象——编译期构建表达式树，最终一次性求值。Eigen 等矩阵库的核心技术。

## 问题：临时对象

```cpp
// 朴素实现：a + b + c 创建两个临时向量
Vec result = a + b + c;
// 1. temp1 = a + b  （创建临时对象）
// 2. result = temp1 + c  （创建临时对象）
// 3. 两次遍历，两次内存分配
```

## 表达式模板解决

```cpp
// 加法表达式（不立即求值）
template <typename L, typename R>
struct AddExpr {
    const L& lhs;
    const R& rhs;
    auto operator[](size_t i) const { return lhs[i] + rhs[i]; }
};

// 向量类
template <typename T>
class Vec {
    std::vector<T> data_;
public:
    // operator+ 返回表达式对象，不计算
    template <typename R>
    AddExpr<Vec, R> operator+(const R& rhs) const {
        return {*this, rhs};
    }

    // 赋值时才求值——遍历一次，无临时对象
    template <typename E>
    Vec& operator=(const E& expr) {
        for (size_t i = 0; i < data_.size(); ++i)
            data_[i] = expr[i];
        return *this;
    }
};

// Vec result = a + b + c;
// 编译期构建 AddExpr<AddExpr<Vec, Vec>, Vec>
// 求值时一次遍历：result[i] = a[i] + b[i] + c[i]
```

## 关键要点

> 表达式模板的核心：运算符重载返回表达式对象（而非计算结果），赋值时才一次性求值。消除临时对象、减少内存分配和遍历次数。

> Eigen、Blaze、xtensor 等高性能数学库都使用表达式模板。

## 相关模式 / 关联

- [[cpp-运算符重载]] — 表达式模板的基础
- [[cpp-函数式编程模式深入]] — 惰性求值
