---
title: expression templates 矩阵库实现
tags: [cpp, template, expression-template, eigen, lazy-evaluation, dsl]
aliases: [表达式模板矩阵, Eigen 核心技术, 编译期表达式树]
created: 2026-04-05
updated: 2026-04-05
---

# expression templates 矩阵库实现

**一句话概述：** 表达式模板把 `A + B + C` 的运算符调用在编译期构建成表达式树，赋值时一次性遍历整棵树计算——避免了中间临时对象，性能接近手写循环。这是 Eigen、Blitz++、Boost.UBLAS 的核心技术。

## 问题：朴素实现的开销

```cpp
Matrix result = A + B + C;
// 朴素实现：
// temp1 = A + B        → 遍历一次，分配临时矩阵
// result = temp1 + C   → 遍历一次
// 共 2 次遍历 + 1 次临时分配

// 表达式模板：
// for (i) result[i] = A[i] + B[i] + C[i]  → 1 次遍历，零临时分配
```

## 核心实现

```cpp
#include <cstddef>
#include <algorithm>

template <typename E>
class VecExpression {
public:
    double operator[](size_t i) const {
        return static_cast<const E&>(*this)[i];
    }
    size_t size() const {
        return static_cast<const E&>(*this).size();
    }
};

// 实际向量
class Vector : public VecExpression<Vector> {
    double* data_;
    size_t size_;
public:
    Vector(size_t n) : data_(new double[n]), size_(n) {}
    Vector(const Vector& v) : data_(new double[v.size_]), size_(v.size_) {
        std::copy_n(v.data_, size_, data_);
    }
    ~Vector() { delete[] data_; }

    double operator[](size_t i) const { return data_[i]; }
    double& operator[](size_t i) { return data_[i]; }
    size_t size() const { return size_; }

    // 关键：从表达式模板赋值
    template <typename E>
    Vector& operator=(const VecExpression<E>& expr) {
        for (size_t i = 0; i < size_; ++i)
            data_[i] = expr[i];  // 逐元素计算，无临时对象
        return *this;
    }
};

// 加法表达式（不计算，只存储引用）
template <typename E1, typename E2>
class AddExpr : public VecExpression<AddExpr<E1, E2>> {
    const E1& lhs_;
    const E2& rhs_;
public:
    AddExpr(const E1& lhs, const E2& rhs) : lhs_(lhs), rhs_(rhs) {}
    double operator[](size_t i) const { return lhs_[i] + rhs_[i]; }
    size_t size() const { return lhs_.size(); }
};

// 运算符返回表达式对象（不是计算结果）
template <typename E1, typename E2>
AddExpr<E1, E2> operator+(const VecExpression<E1>& a, const VecExpression<E2>& b) {
    return {static_cast<const E1&>(a), static_cast<const E2&>(b)};
}

// 使用
Vector a(1000), b(1000), c(1000), d(1000), result(1000);
result = a + b + c + d;
// 编译器看到的是：result[i] = a[i] + b[i] + c[i] + d[i]
// 1 次循环，零临时对象
```

## 关键要点

> 表达式模板的核心是"延迟求值"——运算符不计算结果，而是构建一个记录操作的数据结构。赋值时才一次性计算。

> 代价：编译时间增加（每种运算组合都实例化新模板）、代码膨胀（每种表达式类型都有独立的代码路径）。

## 相关模式 / 关联

- [[cpp-表达式模板]] — 表达式模板基础
- [[cpp-运算符重载]] — 运算符重载技巧
- [[cpp-CRTP奇异递归模板模式]] — CRTP 与表达式模板常配合
- [[cpp-编译期计算与constexpr深入]] — 编译期计算
