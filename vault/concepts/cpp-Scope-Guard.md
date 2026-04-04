---
title: C++ Scope Guard
tags: [cpp, scope-guard, RAII, cleanup, finally, defer]
aliases: [Scope Guard, scope_exit, 作用域守卫, cleanup, defer]
created: 2026-04-04
updated: 2026-04-04
---

# Scope Guard

Scope Guard 在离开作用域时自动执行清理操作——类似 Go 的 `defer`，是异常安全清理的利器。

## 基本实现

```cpp
template <typename F>
class ScopeGuard {
    F func_;
    bool active_;
public:
    explicit ScopeGuard(F func) : func_(std::move(func)), active_(true) {}
    ~ScopeGuard() { if (active_) func_(); }

    void dismiss() { active_ = false; }

    ScopeGuard(ScopeGuard&& other) noexcept
        : func_(std::move(other.func_)), active_(other.active_) {
        other.active_ = false;
    }

    ScopeGuard(const ScopeGuard&) = delete;
    ScopeGuard& operator=(const ScopeGuard&) = delete;
};

template <typename F>
ScopeGuard<F> make_guard(F func) {
    return ScopeGuard<F>(std::move(func));
}
```

## 使用

```cpp
void process() {
    auto conn = database.connect();
    auto guard = make_guard([&] { conn.close(); });  // 保证关闭

    conn.execute("BEGIN");
    auto txn_guard = make_guard([&] { conn.execute("ROLLBACK"); });

    do_work();  // 可能抛异常

    txn_guard.dismiss();  // 成功，不回滚
    conn.execute("COMMIT");
    // guard 析构时关闭连接
}
```

## C++26: std::scope_exit/std::scope_success/std::scope_fail

```cpp
#include <scope>  // C++26

void process() {
    auto file = fopen("data.txt", "r");
    std::scope_exit cleanup([&] { fclose(file); });

    // std::scope_success：只在成功时执行
    // std::scope_fail：只在异常时执行
}
```

## 关键要点

> Scope Guard 的 `dismiss()` 在成功时取消清理——异常路径自动执行清理，正常路径手动 dismiss。

> C++ 中实现 defer 语义的标准方式就是 Scope Guard——不需要等标准库，自己写也很简单。

## 相关模式 / 关联

- [[cpp-raii-惯用法]] — RAII 是 Scope Guard 的基础
- [[cpp-异常安全深入]] — 异常安全清理
