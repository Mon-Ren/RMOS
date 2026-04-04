---
title: 友元与静态成员
tags: [cpp, oop, friend, static-member, class-design]
aliases: [友元, friend, 静态成员, static member, 类静态, 友元函数]
created: 2026-04-04
updated: 2026-04-04
---

# 友元与静态成员

友元打破封装授予访问权，静态成员让数据或函数属于类而非对象——两者都是类设计的特殊工具。

## 友元

```cpp
class Matrix {
    double data_[4][4];
public:
    // 友元函数：可以访问私有成员
    friend Matrix operator*(const Matrix& a, const Matrix& b);
    friend std::ostream& operator<<(std::ostream& os, const Matrix& m);
};

// 友元不是成员函数，不加 Matrix:: 前缀
Matrix operator*(const Matrix& a, const Matrix& b) {
    Matrix result;
    for (int i = 0; i < 4; ++i)
        for (int j = 0; j < 4; ++j) {
            result.data_[i][j] = 0;  // 可以直接访问私有成员
            for (int k = 0; k < 4; ++k)
                result.data_[i][j] += a.data_[i][k] * b.data_[k][j];
        }
    return result;
}

// 友元类
class Builder {
public:
    void configure(Widget& w) {
        w.private_member = 42;  // Builder 可访问 Widget 的私有成员
    }
};

class Widget {
    int private_member;
    friend class Builder;  // 整个 Builder 类都是友元
};
```

## 静态成员

```cpp
class Counter {
    static int count_;             // 声明（不分配存储）
    static constexpr int MAX = 100; // 内联静态常量（C++17）

public:
    Counter() { ++count_; }
    ~Counter() { --count_; }

    // 静态成员函数：不依赖 this
    static int getCount() { return count_; }
    // 不能声明为 const（没有 this）
    // 不能声明为 virtual
};

int Counter::count_ = 0;  // 定义（分配存储），放在 .cpp 文件中

// C++17: inline 变量（头文件中定义）
class Config {
    static inline std::string default_name = "unnamed";  // 头文件中即可
};

// 使用
Counter a, b;
Counter::getCount();  // 2
```

## 关键要点

> 友元破坏封装——只在运算符重载等少数场景使用，且只授予最小必要权限。友元关系不可传递、不可继承。

> 静态成员函数没有 `this` 指针，不能访问非静态成员，不能声明为 const 或 virtual。

## 相关模式 / 关联

- [[cpp-运算符重载]] — 友元函数的常见用途
- [[cpp-类与对象]] — 类的基础
