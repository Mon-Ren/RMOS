---
title: Expression Templates 表达式模板
tags: [cpp, idiom, expression-template, template, performance]
aliases: [Expression Templates, 表达式模板, 延迟求值, lazy evaluation, proxy object]
created: 2026-04-04
updated: 2026-04-04
---

# Expression Templates 表达式模板

**一句话概述：** 运算符重载返回代理对象而非结果，将整个表达式构建为编译时类型，赋值时一次性求值——避免中间临时对象，实现零开销的向量/矩阵运算（Eigen 库的核心技术）。

## 意图与场景

表达式模板解决"运算符链式调用产生大量临时对象"的问题：

- **延迟求值**：`a + b + c` 不创建中间 `a+b` 的临时结果
- **编译时表达式树**：每个运算符返回一个代理类型，记录操作
- **赋值时融合求值**：在 `=` 时遍历表达式树，一步完成所有运算
- **自动向量化**：连续内存访问模式有利于 SIMD 优化

**适用场景：**
- 数值计算库（BLAS、线性代数）
- 矩阵/向量运算（Eigen、Blaze）
- 字符串拼接优化
- 任何"链式操作产生中间结果"的场景

## C++ 实现代码

### 简化的向量表达式模板

```cpp
#include <vector>
#include <iostream>
#include <cstddef>
#include <cmath>

// 前向声明
template <typename E> class VectorExpression;

// 向量类
class Vector {
    std::vector<double> data_;

public:
    explicit Vector(std::size_t n) : data_(n) {}
    Vector(std::initializer_list<double> init) : data_(init) {}
    
    template <typename E>
    Vector(const VectorExpression<E>& expr);  // 从表达式赋值
    
    double  operator[](std::size_t i) const { return data_[i]; }
    double& operator[](std::size_t i)       { return data_[i]; }
    std::size_t size() const { return data_.size(); }
    
    const std::vector<double>& data() const { return data_; }
};

// 表达式基类（CRTP）
template <typename E>
class VectorExpression {
public:
    double operator[](std::size_t i) const {
        return static_cast<const E&>(*this)[i];
    }
    std::size_t size() const {
        return static_cast<const E&>(*this).size();
    }
};

// Vector 本身也是一个表达式
// （隐式继承 VectorExpression<Vector>，简化起见这里省略）

// 加法表达式代理
template <typename LHS, typename RHS>
class VectorAdd : public VectorExpression<VectorAdd<LHS, RHS>> {
    const LHS& lhs_;
    const RHS& rhs_;

public:
    VectorAdd(const LHS& lhs, const RHS& rhs) : lhs_(lhs), rhs_(rhs) {}
    
    double operator[](std::size_t i) const {
        return lhs_[i] + rhs_[i];  // 延迟：到这里才真正计算
    }
    std::size_t size() const { return lhs_.size(); }
};

// 标量乘法代理
template <typename E>
class VectorScale : public VectorExpression<VectorScale<E>> {
    const E& expr_;
    double scalar_;

public:
    VectorScale(const E& expr, double s) : expr_(expr), scalar_(s) {}
    
    double operator[](std::size_t i) const {
        return expr_[i] * scalar_;
    }
    std::size_t size() const { return expr_.size(); }
};

// 运算符重载：返回代理对象，而非计算结果
template <typename LHS, typename RHS>
VectorAdd<LHS, RHS> operator+(const VectorExpression<LHS>& lhs,
                               const VectorExpression<RHS>& rhs) {
    return VectorAdd<LHS, RHS>(
        static_cast<const LHS&>(lhs),
        static_cast<const RHS&>(rhs)
    );
}

template <typename E>
VectorScale<E> operator*(const VectorExpression<E>& expr, double s) {
    return VectorScale<E>(static_cast<const E&>(expr), s);
}

// 赋值时：遍历表达式树，一次求值
template <typename E>
Vector::Vector(const VectorExpression<E>& expr) : data_(expr.size()) {
    for (std::size_t i = 0; i < expr.size(); ++i) {
        data_[i] = expr[i];  // 每个元素只访问一次
    }
}

// 使用
void demo() {
    Vector a = {1.0, 2.0, 3.0};
    Vector b = {4.0, 5.0, 6.0};
    Vector c = {7.0, 8.0, 9.0};
    
    // 无中间临时对象！
    // result[i] = (a[i] + b[i]) * 2.0 + c[i] 一次完成
    Vector result = (a + b) * 2.0 + c;
    
    for (std::size_t i = 0; i < result.size(); ++i) {
        std::cout << result[i] << " ";  // 7 11 15
    }
}
```

### 字符串拼接优化（简化版）

```cpp
#include <string>
#include <sstream>

// 传统方式：N 个字符串 → N-1 个临时 std::string
// std::string result = a + b + c + d;  // 3 个临时对象

// 表达式模板方式：延迟拼接，一次性分配+拷贝
class LazyString {
    std::vector<std::string_view> parts_;
    
public:
    LazyString(std::string_view sv) { parts_.push_back(sv); }
    
    LazyString operator+(std::string_view other) const {
        LazyString result = *this;
        result.parts_.push_back(other);
        return result;
    }
    
    // 最终求值：一次性分配+拼接
    std::string str() const {
        std::size_t total = 0;
        for (auto& p : parts_) total += p.size();
        
        std::string result;
        result.reserve(total);
        for (auto& p : parts_) result.append(p);
        return result;
    }
    
    // 隐式转换
    operator std::string() const { return str(); }
};
```

## 优缺点

| 优点 | 缺点 |
|------|------|
| 消除中间临时对象 | 代码复杂度极高 |
| 编译时表达式融合 | 编译时间显著增加 |
| 自动向量化友好 | 调试困难（类型名爆炸） |
| 性能接近手写循环 | 引用悬挂风险（代理对象持有引用） |

> [!tip] 关键要点
> 表达式模板是**编译时优化**的极致——将运行时的"多次计算+多次临时对象"转化为编译时的"一次循环+无临时对象"。Eigen 库通过此技术实现了接近手写 BLAS 的性能。除非你在写数值计算库，否则不需要自己实现表达式模板——但它理解它对理解 Eigen 的工作原理至关重要。

> [!warning] 引用悬挂
> 代理对象通常持有表达式各部分的 const 引用。如果某个部分是临时对象：
> ```cpp
> auto expr = Vector{1,2,3} + Vector{4,5,6};  // 两个临时对象
> Vector result = expr;  // 💥 悬挂引用！
> ```
> 必须在同一条语句中完成表达式构建和求值。

## 相关链接

- [[cpp-策略设计]] — 表达式模板中用策略控制求值方式
- [[cpp-crtp-奇异递归模板模式]] — VectorExpression 用 CRTP 实现多态
- [[代理模式]] — 表达式代理是代理模式的编译时应用
