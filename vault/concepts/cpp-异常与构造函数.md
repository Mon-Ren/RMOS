---
title: C++ 异常与构造函数
tags: [cpp, exception, constructor, partially-constructed, RAII]
aliases: [构造函数异常, 构造失败, 部分构造, 构造函数错误处理]
created: 2026-04-04
updated: 2026-04-04
---

# 异常与构造函数

构造函数不能返回错误码——异常是构造函数中报告失败的唯一标准方式。

## 构造函数中的异常

```cpp
class Connection {
    Socket socket_;
    std::string host_;
public:
    Connection(const std::string& host) : host_(host) {
        socket_ = Socket::connect(host);
        if (!socket_.is_valid()) {
            throw std::runtime_error("Connection failed: " + host);
        }
    }
    // 如果抛异常：
    // 1. 对象从未完全构造
    // 2. 已构造的成员（host_）自动析构
    // 3. 析构函数不会被调用
    // 4. RAII 保证资源不泄漏
};
```

## 部分构造的析构规则

```cpp
class Widget {
    std::string name_;        // 先构造
    std::vector<int> data_;   // 后构造
    int* raw_ptr_;            // 危险：异常时可能泄漏
public:
    Widget(const std::string& n) : name_(n), data_{1, 2, 3} {
        raw_ptr_ = new int(42);  // 如果这里抛异常？
        // name_ 和 data_ 已析构，但 raw_ptr_ 泄漏了！
    }
    ~Widget() { delete raw_ptr_; }  // 不会调用——对象未完全构造
};

// 修复：用 unique_ptr 替代裸指针
class SafeWidget {
    std::string name_;
    std::vector<int> data_;
    std::unique_ptr<int> raw_ptr_;  // RAII 管理
public:
    SafeWidget(const std::string& n)
        : name_(n), data_{1, 2, 3}, raw_ptr_(std::make_unique<int>(42)) {}
    // 如果任何成员构造失败，已构造的成员自动析构
};
```

## 委托构造中的异常

```cpp
class Config {
    std::string path_;
    int timeout_;
public:
    Config(const std::string& p, int t) : path_(p), timeout_(t) {
        if (t < 0) throw std::invalid_argument("negative timeout");
    }

    // 委托构造：如果被委托的构造抛异常，当前构造也终止
    Config() : Config("default.conf", 30) {}
    // 如果 Config("default.conf", 30) 抛异常，Config() 也抛异常
};
```

## 关键要点

> 构造函数中抛异常时，已完全构造的成员会自动析构，但析构函数本身不会被调用（因为对象从未"存在"）。

> 用 RAII 成员管理资源（unique_ptr、string、vector）——构造函数异常时自动清理。避免裸指针成员。

## 相关模式 / 关联

- [[cpp-异常处理]] — 异常基础
- [[cpp-raii-惯用法]] — 构造函数异常的基石
