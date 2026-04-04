---
title: C++ 函数返回多个值
tags: [cpp, multiple-return, tuple, pair, structured-binding, output-parameter]
aliases: [多返回值, 返回tuple, 返回pair, 结构化绑定返回, output参数]
created: 2026-04-04
updated: 2026-04-04
---

# C++ 函数返回多个值

C++ 有多种方式从函数返回多个值——选择取决于可读性和性能需求。

## 方案对比

```cpp
// 方案 1：struct（推荐，最具可读性）
struct ParseResult {
    bool success;
    int value;
    std::string error;
};

ParseResult parse(const std::string& s) {
    if (s.empty()) return {false, 0, "empty"};
    return {true, std::stoi(s), ""};
}
auto [ok, val, err] = parse("42");

// 方案 2：pair（两个值时简洁）
std::pair<bool, int> find(const std::vector<int>& v, int target) {
    for (size_t i = 0; i < v.size(); ++i)
        if (v[i] == target) return {true, static_cast<int>(i)};
    return {false, -1};
}
auto [found, idx] = find(v, 42);

// 方案 3：optional（可能没有值）
std::optional<int> find(const std::vector<int>& v, int target);

// 方案 4：expected（成功值或错误）
std::expected<int, std::string> parse(const std::string& s);

// 方案 5：output 参数（C 风格，不推荐）
void compute(int input, int* output1, double* output2);
```

## 选择指南

```
返回 1 个可选值         → optional
返回 2 个值             → pair 或 struct
返回 3+ 个值            → struct
可能失败 + 错误信息      → expected
性能关键 + 已有 output 参数风格 → output 参数（不推荐新代码）
```

## 关键要点

> struct 返回值配合结构化绑定是最佳方案——可读性最好、自文档化、NRVO 优化零开销。

> `pair` 适合只有两个值且关系明确的场景（如 find 返回 {found, index}）。

## 相关模式 / 关联

- [[cpp-结构化绑定]] — 解构返回值
- [[cpp-optional]] — optional 方案
- [[cpp-expected]] — expected 方案
