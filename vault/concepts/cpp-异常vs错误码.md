---
title: 异常 vs 错误码
tags: [cpp, error-handling, exception, error-code, expected, strategy]
aliases: [异常vs错误码, 错误处理策略, error code, error handling, 错误传播]
created: 2026-04-04
updated: 2026-04-04
---

# 异常 vs 错误码

C++ 有两种主流错误处理方式——选择哪种取决于你的领域和约束。

## 异常

```cpp
// 优势：自动传播，不污染正常路径
Widget load(const std::string& path) {
    auto file = open(path);        // 可能抛异常
    auto data = parse(file);       // 可能抛异常
    return build(data);            // 可能抛异常
    // 如果任何步骤失败，自动传播到调用者
    // 不需要每步检查返回值
}

// 代价：
// 1. 二进制体积增大（异常表）
// 2. 不确定性（抛异常时的栈展开开销）
// 3. 某些领域禁用异常（嵌入式、实时系统、游戏引擎）
// 4. 编译器可能不做某些优化
```

## 错误码

```cpp
// 优势：确定性、无隐式控制流
std::expected<Widget, ErrorCode> load(const std::string& path) {
    auto file = open(path);
    if (!file) return std::unexpected(file.error());

    auto data = parse(*file);
    if (!data) return std::unexpected(data.error());

    return build(*data);
}

// 代价：
// 1. 每步都需要检查（容易忘记）
// 2. 错误传播需要手动转发
// 3. 正常逻辑和错误处理混在一起
```

## 如何选择

```
场景                              推荐
───────────────────────────────────────
通用应用代码                       异常
高性能/实时系统                    错误码/expected
嵌入式/禁用异常环境                错误码/expected
库的公共接口                       expected（避免异常泄漏）
构造函数失败                       异常（构造函数无法返回值）
深层次调用中的错误                 异常（自动传播）
预期内的失败（解析、查找）         expected
不可恢复的错误（OOM、断言失败）    异常
```

## 混合策略

```cpp
// 对外接口用 expected，内部用异常
class Parser {
public:
    // 公共接口：expected（不泄露异常）
    std::expected<AST, ParseError> parse(std::string_view input) {
        try {
            return parse_impl(input);  // 内部可能抛异常
        } catch (const SyntaxError& e) {
            return std::unexpected(ParseError{e.what()});
        }
    }

private:
    AST parse_impl(std::string_view input) {
        // 内部可以用异常简化错误处理
        if (!valid(input)) throw SyntaxError("...");
        // ...
    }
};
```

## 关键要点

> 异常和错误码不是互斥的——可以根据场景选择。`std::expected` 是错误码的现代实现，解决了 C 风格错误码的大部分问题。

> 程序中应该统一一种策略——不要在同一个模块中混用异常和返回值检查。

## 相关模式 / 关联

- [[cpp-异常处理]] — 异常的详细使用
- [[cpp-expected]] — C++23 的错误码类型
