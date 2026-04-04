---
title: 引用限定成员函数
tags: [cpp, ref-qualifier, lvalue-rvalue, member-function, this-qualifier]
aliases: [引用限定, ref-qualifier, lvalue限定, rvalue限定, &与&&限定]
created: 2026-04-04
updated: 2026-04-04
---

# 引用限定成员函数

引用限定让成员函数根据调用对象是左值还是右值选择不同实现——防止对临时对象调用"修改后不读"的操作。

## 问题

```cpp
class String {
public:
    String operator+(const String& rhs) const &;  // 左值版本
    String operator+(const String& rhs) &&;        // 右值版本（修改自身）
};

String a = "hello", b = "world";
String c = a + b;          // 左值 a，调用 const & 版本
String d = std::move(a) + b;  // 右值 a，调用 && 版本（复用 a 的内存）

// 经典问题：防止返回右值容器的元素引用
std::vector<int> get_vec();
// get_vec()[0] = 42;  // 危险：临时对象的引用！
```

## 语法

```cpp
class Widget {
    std::string data_;
public:
    // const & 版本：左值对象调用
    const std::string& data() const & { return data_; }

    // && 版本：右值对象调用（可以移动）
    std::string data() && { return std::move(data_); }

    // 非 const & 版本
    std::string& data() & { return data_; }
};

Widget w;
w.data();              // 调用 & 版本

Widget make_widget();
make_widget().data();  // 调用 && 版本（移动语义）
```

## 实际应用

```cpp
class Config {
    std::map<std::string, std::string> data_;
public:
    // 修正链式调用的临时对象问题
    Config&& build() && {
        validate();
        return std::move(*this);
    }
};

auto config = Config{}.set("a", "1").set("b", "2").build();
// 确保只在右值上使用
```

## 关键要点

> 引用限定是 const 的补充——const 区分"是否修改"，引用限定区分"左值/右值"。它让类的接口更精确地表达意图。

> 大多数项目不常用引用限定——只有在移动语义优化或防止误用时才需要。

## 相关模式 / 关联

- [[cpp-右值引用与移动语义]] — 引用限定的应用
- [[cpp-运算符重载]] — 运算符的引用限定
