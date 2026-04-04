---
title: 异常安全深入
tags: [cpp, exception-safety, basic-guarantee, strong-guarantee, noexcept]
aliases: [异常安全, basic guarantee, strong guarantee, 异常安全级别, 异常安全设计]
created: 2026-04-04
updated: 2026-04-04
---

# 异常安全深入

异常安全不是"捕获异常"，而是保证异常发生时程序状态仍然正确——每个函数都需要明确自己的异常安全级别。

## 四个级别

```
无安全保证    — 泄露资源或破坏不变量
基本保证      — 不泄露资源，对象处于有效但不确定状态
强保证        — 操作要么完全成功，要么状态不变（commit-or-rollback）
不抛异常保证  — 承诺不抛异常（noexcept）
```

## 基本保证

```cpp
// 基本保证：即使抛异常，资源不泄露
class Document {
    std::vector<std::string> lines_;
    FILE* log_file_;
public:
    void add_line(const std::string& line) {
        lines_.push_back(line);       // 可能抛异常（bad_alloc）
        fprintf(log_file_, "added\n"); // push_back 成功后才执行
        // 如果 fprintf 抛（不太可能），lines_ 已更新——这是基本保证
    }
};
```

## 强保证

```cpp
// 强保证：先在临时对象上操作，成功后 swap
class Config {
    std::map<std::string, std::string> settings_;
public:
    void update(const std::string& key, const std::string& val) {
        auto copy = settings_;          // 拷贝当前状态
        copy[key] = val;                // 在拷贝上修改（可能抛）
        settings_.swap(copy);           // swap 不抛异常
    }
    // 如果 copy[key] = val 抛异常，settings_ 不变——强保证
};

// copy-and-swap 实现强保证的赋值
Config& operator=(Config other) {  // 参数按值传递（拷贝在这里发生）
    swap(other);                    // swap 不抛
    return *this;
    // other 析构释放旧资源
}
```

## 设计原则

```cpp
// 原则 1：先做可能失败的操作，再做不可逆的操作
void transfer(Account& from, Account& to, int amount) {
    // 1. 先做所有可能失败的检查和计算
    if (from.balance < amount) throw InsufficientFunds();
    int new_from = from.balance - amount;  // 计算新值
    int new_to = to.balance + amount;

    // 2. 再做不可逆操作（标记 noexcept）
    from.balance = new_from;  // 简单赋值，不抛异常
    to.balance = new_to;
}

// 原则 2：析构函数不抛异常
~Resource() {
    try { cleanup(); }
    catch (...) { /* 记录日志，不传播 */ }
    // 析构中抛异常 → 如果正在栈展开 → std::terminate
}
```

## 关键要点

> 函数的异常安全级别应该写在文档注释里。调用者需要知道如果函数抛异常，系统状态是否保持一致。

> 强保证的实现通常需要先拷贝/计算再 swap——swap 必须是 noexcept。

## 相关模式 / 关联

- [[cpp-异常处理]] — 异常基础
- [[cpp-Rule-of-Zero与Rule-of-Five]] — 异常安全的特殊成员函数
