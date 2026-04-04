---
title: 属性（Attributes）
tags: [cpp, attributes, nodiscard, maybe_unused, deprecated, likely]
aliases: [属性, attributes, nodiscard, maybe_unused, deprecated, likely, unlikely]
created: 2026-04-04
updated: 2026-04-04
---

# 属性（Attributes）

属性是给编译器的元信息——不影响程序语义，但帮助编译器优化和给出更好的诊断。

## 标准属性

```cpp
// C++17: [[nodiscard]]——忽略返回值时警告
[[nodiscard]] int compute();  // 返回值不应该被忽略
compute();  // ⚠️ 警告：忽略了 nodiscard 的返回值
int r = compute();  // OK

// [[nodiscard]] 加理由
[[nodiscard("资源泄漏")]] std::unique_ptr<Widget> create();
create();  // 警告：资源泄漏

// C++17: [[maybe_unused]]——抑制未使用警告
[[maybe_unused]] int debug_value = compute();  // 不产生"未使用"警告

// C++14: [[deprecated]]——标记弃用
[[deprecated("使用 new_api 代替")]]
void old_api();

old_api();  // ⚠️ 警告：函数已弃用

// C++20: [[likely]] / [[unlikely]]——分支概率提示
if (result) [[likely]] {
    // 编译器可能优化此分支的布局
} else [[unlikely]] {
    // 编译器可能将此分支放到冷路径
}

// C++20: [[no_unique_address]]——空成员不占空间
struct Config {
    [[no_unique_address]] Allocator alloc;  // 如果 Allocator 是空类，不占空间
    int value;
};
// sizeof(Config) == sizeof(int) 如果 Allocator 是空类

// C++20: [[nodiscard]] 对类/枚举
struct [[nodiscard]] ErrorCode {
    int code;
};
ErrorCode try_something();  // 返回 ErrorCode 类型时忽略会警告
```

## 关键要点

> `[[nodiscard]]` 是最有用的属性——它捕捉了大量"忘记检查返回值"的 bug。对函数、类和枚举都可以使用。

> `[[likely]]` 和 `[[unlikely]]` 是优化提示，不是保证——编译器可以忽略。

## 相关模式 / 关联

- [[cpp-异常处理]] — nodiscard 与异常的配合
- [[cpp-optional]] — 返回 optional 的函数标记 nodiscard
