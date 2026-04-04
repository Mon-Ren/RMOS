---
title: 正则表达式
tags: [cpp, regex, pattern-matching, search, replace]
aliases: [regex, 正则表达式, 模式匹配, smatch, regex_search, regex_replace]
created: 2026-04-04
updated: 2026-04-04
---

# std::regex（C++11）

`std::regex` 提供 C++ 标准的正则表达式——语法灵活但性能不如专用库，复杂场景考虑 PCRE2 或 RE2。

## 基本用法

```cpp
#include <regex>
#include <string>

// 匹配（完整匹配）
std::string email = "user@example.com";
std::regex pattern(R"(\w+@\w+\.\w+)");  // 原始字符串避免转义
bool is_valid = std::regex_match(email, pattern);  // true

// 提取分组
std::string line = "Name: Alice, Age: 25";
std::regex re(R"(Name: (\w+), Age: (\d+))");
std::smatch match;

if (std::regex_search(line, match, re)) {
    std::cout << match[0] << "\n";  // 完整匹配："Name: Alice, Age: 25"
    std::cout << match[1] << "\n";  // 第1组："Alice"
    std::cout << match[2] << "\n";  // 第2组："25"
}

// 搜索（找第一个匹配）
std::string text = "abc 123 def 456";
std::regex num_re(R"(\d+)");
std::smatch m;
if (std::regex_search(text, m, num_re)) {
    std::cout << m[0];  // "123"
}

// 替换
std::string result = std::regex_replace(text, std::regex(R"(\d+)"), "NUM");
// result: "abc NUM def NUM"

// 迭代查找所有匹配
auto begin = std::sregex_iterator(text.begin(), text.end(), num_re);
auto end = std::sregex_iterator();
for (auto it = begin; it != end; ++it) {
    std::cout << (*it)[0] << "\n";  // "123", "456"
}
```

## 常用语法

```
.       任意字符（不含换行）
*       0 或多次
+       1 或多次
?       0 或 1 次
{n,m}   n 到 m 次
\d      数字 [0-9]
\w      单词字符 [a-zA-Z0-9_]
\s      空白字符
\b      单词边界
^       行首
$       行尾
(...)   捕获分组
(?:...) 非捕获分组
|       或
```

## 关键要点

> `std::regex` 编译正则表达式很慢（毫秒级）——不要在循环中反复编译。对于性能敏感场景，提前编译并复用 `std::regex` 对象，或使用 PCRE2/RE2 库。

> `smatch` 用于 `std::string`，`cmatch` 用于 `const char*`。宽字符版本用 `wregex`/`wsmatch`。

## 相关模式 / 关联

- [[cpp-string深入]] — string 的操作
- [[cpp-stl算法总览]] — 算法与正则的配合
