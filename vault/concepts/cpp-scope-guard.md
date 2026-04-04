---
title: Scope Guard
tags: [cpp, idiom, scope-guard, exception-safety]
aliases: [Scope Guard, 作用域守卫, scope_exit, scope_success, scope_fail]
created: 2026-04-04
updated: 2026-04-04
---

# Scope Guard

**一句话概述：** 注册一个在作用域退出时（无论正常退出还是异常退出）自动执行的清理回调——RAII 的泛化形式。

## 意图与场景

Scope Guard 解决"临时需要清理但不想为此写 RAII 类"的问题：

- **延迟执行清理操作**：注册后，离开作用域自动执行
- **异常安全**：即使抛异常，清理也会执行
- **比 try-catch 更优雅**：不需要嵌套 try 块

**适用场景：**
- 多步操作中中间步骤失败时的回滚
- C API 的资源释放（如 `sqlite3_close`）
- 临时修改状态后恢复
- 事务性操作

## C++ 实现代码

### 手动实现 Scope Guard

```cpp
#include <utility>
#include <type_traits>
#include <exception>

template <typename F>
class ScopeGuard {
    F func_;
    bool active_;

public:
    explicit ScopeGuard(F func) 
        : func_(std::move(func)), active_(true) {}
    
    ~ScopeGuard() {
        if (active_) func_();
    }
    
    // 移动
    ScopeGuard(ScopeGuard&& other) noexcept 
        : func_(std::move(other.func_)), active_(other.active_) {
        other.active_ = false;
    }
    
    // 禁止拷贝
    ScopeGuard(const ScopeGuard&) = delete;
    ScopeGuard& operator=(const ScopeGuard&) = delete;
    
    // 提前取消
    void dismiss() noexcept { active_ = false; }
};

// 工厂函数
template <typename F>
ScopeGuard<F> make_scope_guard(F func) {
    return ScopeGuard<F>(std::move(func));
}

// 宏简化（可选）
#define SCOPE_EXIT(code) \
    auto _scope_guard_##__LINE__ = make_scope_guard([&]{ code })
```

### 异常安全的多步操作

```cpp
#include <iostream>
#include <vector>
#include <stdexcept>
#include <cstdio>

// 经典示例：安全的多步骤事务
void multi_step_transaction() {
    std::vector<int> data;
    
    // 步骤 1
    data.push_back(1);
    auto guard1 = make_scope_guard([&] { 
        if (!data.empty()) std::cout << "Rollback step 1\n"; 
    });
    
    // 步骤 2
    data.push_back(2);
    auto guard2 = make_scope_guard([&] {
        std::cout << "Rollback step 2\n";
    });
    
    // 步骤 3 —— 如果这里抛异常，guard2 和 guard1 按逆序执行
    if (/* 条件失败 */ false) {
        throw std::runtime_error("Step 3 failed");
    }
    
    // 全部成功，取消清理
    guard2.dismiss();
    guard1.dismiss();
    std::cout << "Transaction committed\n";
}

// C API 资源管理
void safe_file_ops() {
    auto* fp = std::fopen("data.txt", "r");
    if (!fp) return;
    
    auto guard = make_scope_guard([&] { std::fclose(fp); });
    
    // 安全地使用 fp...
    // 即使抛异常，文件也会关闭
    char buf[256];
    while (std::fgets(buf, sizeof(buf), fp)) {
        // 处理数据
    }
    
    // guard 析构时自动 fclose
}
```

### Scope Exit / Scope Fail / Scope Success

```cpp
#include <exception>

enum class ScopeGuardMode {
    Exit,    // 无论是否异常都执行
    Fail,    // 仅在异常时执行
    Success  // 仅在正常退出时执行
};

template <typename F, ScopeGuardMode Mode = ScopeGuardMode::Exit>
class TypedScopeGuard {
    F func_;
    bool active_;
    int uncaught_;

public:
    explicit TypedScopeGuard(F func)
        : func_(std::move(func))
        , active_(true)
        , uncaught_(std::uncaught_exceptions()) {}
    
    ~TypedScopeGuard() noexcept {
        if (!active_) return;
        
        bool should_run = false;
        if constexpr (Mode == ScopeGuardMode::Exit) {
            should_run = true;
        } else if constexpr (Mode == ScopeGuardMode::Fail) {
            should_run = std::uncaught_exceptions() > uncaught_;
        } else {
            should_run = std::uncaught_exceptions() <= uncaught_;
        }
        
        if (should_run) func_();
    }
    
    void dismiss() noexcept { active_ = false; }
    
    TypedScopeGuard(TypedScopeGuard&& o) noexcept
        : func_(std::move(o.func_)), active_(o.active_), uncaught_(o.uncaught_) {
        o.active_ = false;
    }
    
    TypedScopeGuard(const TypedScopeGuard&) = delete;
    TypedScopeGuard& operator=(const TypedScopeGuard&) = delete;
};

// 工厂函数
template <typename F>
auto on_scope_exit(F f) { return TypedScopeGuard<F, ScopeGuardMode::Exit>(std::move(f)); }

template <typename F>
auto on_scope_fail(F f) { return TypedScopeGuard<F, ScopeGuardMode::Fail>(std::move(f)); }

template <typename F>
auto on_scope_success(F f) { return TypedScopeGuard<F, ScopeGuardMode::Success>(std::move(f)); }
```

### 使用示例

```cpp
void transactional_update() {
    auto conn = acquire_connection();
    
    auto cleanup = on_scope_exit([&] { release_connection(conn); });
    auto rollback = on_scope_fail([&] { conn->rollback(); });
    auto log_success = on_scope_success([&] { log("Update committed"); });
    
    conn->begin();
    conn->execute("UPDATE ...");
    conn->execute("INSERT ...");
    // 抛异常 → rollback 执行 + cleanup 执行
    // 成功 → log_success 执行 + cleanup 执行
}
```

## 优缺点

| 优点 | 缺点 |
|------|------|
| 比 try-catch 更简洁 | 多个 guard 的执行顺序依赖声明顺序 |
| 异常安全保证 | lambda 捕获可能引入悬挂引用 |
| 灵活（exit/fail/success） | 编译错误信息不直观 |
| 不需要专门的 RAII 类 | dismiss() 调用容易遗漏 |

> [!tip] 关键要点
> Scope Guard 是 **RAII 的补充而非替代**。RAII 用于"管理一种资源的所有权"，Scope Guard 用于"临时需要执行清理操作"的场景。C++26 标准（P0052）已将 `scope_exit`、`scope_success`、`scope_fail` 纳入标准库（`<experimental/scope>`）。当前可用 `<experimental/scope>` 或 Boost.Scope。

## 相关链接

- [[cpp-raii-惯用法]] — Scope Guard 是 RAII 的泛化
- [[cpp-智能指针详解]] — unique_ptr 自定义删除器也具备 scope guard 功能
- [[cpp-移动语义]] — Scope Guard 需要支持移动
