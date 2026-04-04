---
title: C++ 模板友元与友元函数
tags: [cpp, template, friend, friend-function, CRTP]
aliases: [模板友元, friend template, 友元模板, 模板友元函数]
created: 2026-04-04
updated: 2026-04-04
---

# 模板友元

模板类的友元声明需要特殊语法——让特定模板实例成为友元。

## 友元模板实例

```cpp
template <typename T>
class Wrapper {
    T value_;
public:
    // 友元：所有 operator<< 的实例
    template <typename U>
    friend std::ostream& operator<<(std::ostream&, const Wrapper<U>&);

    // 友元：特定实例
    friend class Serializer<Wrapper<T>>;  // 只有 Serializer<Wrapper<T>> 是友元
};

template <typename T>
std::ostream& operator<<(std::ostream& os, const Wrapper<T>& w) {
    return os << w.value_;
}
```

## 友元非模板函数（注入类名）

```cpp
template <typename T>
class Matrix {
    T data_[4][4];
public:
    // 友元非模板函数（每个实例一个）
    friend Matrix operator*(const Matrix& a, const Matrix& b) {
        Matrix result;
        // 可以直接访问 a.data_ 和 b.data_
        return result;
    }
};
// 这个 operator* 定义在类内，每个 Matrix<T> 实例化时生成一份
// 可以通过 ADL 找到
```

## 关键要点

> 模板友元的语法取决于你想让哪个实体成为友元——所有实例、特定实例、还是非模板函数。

> 类内定义的友元函数（非模板）自动成为模板实例的一部分——通过 ADL 可以找到。

## 相关模式 / 关联

- [[cpp-友元与静态成员]] — 友元基础
- [[cpp-模板编程基础]] — 模板基础
