---
title: C++23 deducing this
tags: [cpp23, deducing-this, explicit-object, self, CRTP-alternative]
aliases: [deducing this, 显式对象参数, self参数, CRTP替代]
created: 2026-04-04
updated: 2026-04-04
---

# Deducing this（C++23）

`deducing this` 让 `this` 成为显式参数——消除 const/non-const 重载、简化 CRTP、让递归 lambda 成为可能。

## 消除 const/non-const 重载

```cpp
// 传统方式：需要两个重载
struct Old {
    std::string name_;
    const std::string& name() const { return name_; }
    std::string& name() { return name_; }
};

// C++23：一个函数搞定
struct New {
    std::string name_;
    template <typename Self>
    auto&& name(this Self&& self) {
        return std::forward<Self>(self).name_;
    }
    // const 对象调用 → const string&
    // 非 const 对象调用 → string&
    // 右值调用 → string&&（可以移动）
};
```

## 递归 Lambda

```cpp
// 传统方式：需要 std::function 或 Y 组合子
std::function<int(int)> fib = [&fib](int n) {
    return (n <= 1) ? n : fib(n-1) + fib(n-2);
};

// C++23：简洁的递归
auto fib = [](this auto self, int n) -> int {
    return (n <= 1) ? n : self(n-1) + self(n-2);
};
```

## CRTP 替代

```cpp
// CRTP 需要模板继承
template <typename Derived>
class Printable {
    void print() const {
        static_cast<const Derived*>(this)->print_impl();
    }
};

// C++23 deducing this
struct Printable {
    template <typename Self>
    void print(this const Self& self) {
        std::cout << self.to_string() << "\n";
    }
};
// 任何有 to_string() 的类直接继承 Printable 即可
```

## 关键要点

> `deducing this` 是 C++23 对代码简洁性最大的贡献——它让多份重载合并为一份，让 CRTP 不再需要模板继承。

> `this auto` 或 `this Self&& self` 的语法第一次让 `this` 成为函数签名的一部分。

## 相关模式 / 关联

- [[cpp-crtp-奇异递归模板模式]] — deducing this 的替代对象
- [[cpp-this指针与成员指针]] — this 的传统用法
