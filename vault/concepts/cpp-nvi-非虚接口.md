---
title: NVI 非虚接口惯用法
tags: [cpp, idiom, NVI, virtual, template-method]
aliases: [NVI, Non-Virtual Interface, 非虚接口, Non-Virtual Interface Idiom]
created: 2026-04-04
updated: 2026-04-04
---

# NVI 非虚接口惯用法

**一句话概述：** 公有接口使用非虚函数，由它们调用私有/保护虚函数——在虚函数调用前后插入前置/后置逻辑（日志、校验、加锁）。

## 意图与场景

NVI（Non-Virtual Interface）由 Herb Sutter 推广，是模板方法模式的 C++ 特化：

- **公有非虚函数 = 流程骨架**：定义前置检查、后置处理
- **私有/保护虚函数 = 扩展点**：子类只实现具体步骤
- **控制权在基类**：基类决定何时、如何调用子类实现

**适用场景：**
- 虚函数需要前置/后置钩子（日志、计时、加锁）
- 异常安全边界控制
- 防止子类破坏类不变量
- API 设计中控制扩展点的粒度

## C++ 实现代码

### 基本 NVI 模式

```cpp
#include <iostream>
#include <chrono>
#include <stdexcept>

class DataProcessor {
public:
    // 公有非虚接口——对外提供稳定 API
    void process(const std::string& data) {
        validate(data);           // 前置钩子
        auto start = clock::now();
        
        do_process(data);         // 调用虚函数（扩展点）
        
        auto elapsed = clock::now() - start;
        log_timing(elapsed);      // 后置钩子
    }
    
    bool try_process(const std::string& data) noexcept {
        try {
            process(data);
            return true;
        } catch (...) {
            on_error();           // 错误钩子
            return false;
        }
    }
    
    virtual ~DataProcessor() = default;

private:
    using clock = std::chrono::steady_clock;
    
    void validate(const std::string& data) {
        if (data.empty()) throw std::invalid_argument("Empty data");
    }
    
    void log_timing(clock::duration d) {
        auto ms = std::chrono::duration_cast<std::chrono::milliseconds>(d);
        std::cout << "Process took " << ms.count() << "ms\n";
    }
    
    virtual void on_error() {
        std::cerr << "Processing failed\n";
    }

protected:
    // 子类只需实现这个——纯虚或有默认实现
    virtual void do_process(const std::string& data) = 0;
};

class CsvProcessor : public DataProcessor {
protected:
    void do_process(const std::string& data) override {
        std::cout << "Processing CSV: " << data.substr(0, 20) << "...\n";
        // CSV 特定逻辑
    }
};

class JsonProcessor : public DataProcessor {
protected:
    void do_process(const std::string& data) override {
        std::cout << "Processing JSON: " << data.substr(0, 20) << "...\n";
        // JSON 特定逻辑
    }
};
```

### NVI + 不变量保护

```cpp
class BankAccount {
    double balance_ = 0.0;

public:
    // 非虚接口保证不变量
    void deposit(double amount) {
        if (amount <= 0) throw std::invalid_argument("Negative deposit");
        do_deposit(amount);      // 子类实现
        balance_ += amount;      // 不变量：余额更新
        on_balance_changed();    // 通知钩子
    }
    
    void withdraw(double amount) {
        if (amount <= 0) throw std::invalid_argument("Negative withdrawal");
        if (amount > balance_) throw std::runtime_error("Insufficient funds");
        do_withdraw(amount);
        balance_ -= amount;
        on_balance_changed();
    }
    
    double balance() const noexcept { return balance_; }
    virtual ~BankAccount() = default;

protected:
    virtual void do_deposit(double) {}    // 默认空实现
    virtual void do_withdraw(double) {}   // 默认空实现
    virtual void on_balance_changed() {}  // 可选的观察钩子

private:
    // 子类禁止访问余额修改
};

class SavingsAccount : public BankAccount {
protected:
    void on_balance_changed() override {
        // 奖励积分逻辑
    }
};
```

### NVI 与异常安全

```cpp
class Transaction {
public:
    void execute() {
        begin_transaction();         // 前置：RAII 锁
        try {
            do_execute();            // 扩展点
            commit();                // 后置：提交
        } catch (...) {
            rollback();              // 异常处理：回滚
            throw;
        }
    }

private:
    virtual void do_execute() = 0;
    
    void begin_transaction() { std::cout << "BEGIN\n"; }
    void commit()            { std::cout << "COMMIT\n"; }
    void rollback()          { std::cout << "ROLLBACK\n"; }
};
```

## 优缺点

| 优点 | 缺点 |
|------|------|
| 基类控制虚函数调用时机 | 增加了一层间接调用 |
| 可插入前置/后置逻辑 | 子类不能完全控制行为 |
| 保护类不变量 | 公有虚函数在某些简单场景更直接 |
| 异常安全边界清晰 | 增加了接口层次 |

> [!tip] 关键要点
> NVI 的核心哲学是：**公有接口 = 服务契约（what），私有虚函数 = 实现细节（how）**。Herb Sutter 的建议："Prefer to make public functions non-virtual and virtual functions private (or protected)." 简单的 getter/setter 虚函数不需要 NVI——过度设计同样有害。

> [!info] NVI vs 公有虚函数
> - **公有虚函数**适合简单的 getter、纯接口（纯虚）
> - **NVI**适合需要前后钩子、不变量保护、异常处理的复杂操作
> - **Rule**：如果你在想"调用这个虚函数之前/之后我需要做什么"，就用 NVI

## 相关链接

- [[模板方法模式]] — NVI 是模板方法模式的 C++ 实现
- [[cpp-raii-惯用法]] — NVI 中前置/后置操作常使用 RAII
- [[设计模式-cpp-选型指南]] — 何时选择虚函数 vs 模板
