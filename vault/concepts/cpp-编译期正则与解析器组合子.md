---
title: 编译期正则与解析器组合子
tags: [cpp, constexpr, parser, combinator, compile-time, regex]
aliases: [编译期解析器, constexpr parser, 编译期正则]
created: 2026-04-05
updated: 2026-04-05
---

# 编译期正则与解析器组合子

**一句话概述：** C++20 的 constexpr 足够强大，可以在编译期实现简单的解析器组合子——用函数组合定义文法规则，编译期解析字符串并提取结构化数据。虽然不如运行时正则库灵活，但零运行时开销。

## 示例：编译期 JSON 键查找

```cpp
#include <string_view>

constexpr std::string_view extract_json_value(std::string_view json, std::string_view key) {
    // 简化实现：查找 "key": "value"
    auto pos = json.find("\"" + std::string(key) + "\"");
    if (pos == std::string_view::npos) return "";

    pos = json.find(':', pos);
    if (pos == std::string_view::npos) return "";

    pos = json.find('"', pos + 1);
    if (pos == std::string_view::npos) return "";

    auto end = json.find('"', pos + 1);
    if (end == std::string_view::npos) return "";

    return json.substr(pos + 1, end - pos - 1);
}

constexpr std::string_view config = R"({"host": "localhost", "port": "8080"})";
constexpr auto host = extract_json_value(config, "host");
static_assert(host == "localhost");
```

## 关键要点

> 编译期解析器适合配置验证、命令行解析等场景。复杂解析（完整 JSON、XML）还是用运行时库。constexpr 字符串操作的编译时间随输入长度增长，过长的输入会让编译变慢。

## 相关模式 / 关联

- [[cpp-编译期字符串处理]] — 编译期字符串
- [[cpp-constexpr-分配与编译期容器]] — 编译期容器
- [[cpp-编译期字符串hash与switch-string]] — 编译期 hash
- [[cpp-正则表达式]] — 运行时正则
