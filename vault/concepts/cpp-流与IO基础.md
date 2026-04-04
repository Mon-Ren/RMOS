---
title: 流与 IO 基础
tags: [cpp, iostream, cin, cout, stream, formatted-io]
aliases: [iostream, cin, cout, cerr, 流, 输入输出, 格式化IO]
created: 2026-04-04
updated: 2026-04-04
---

# 流与 IO 基础

C++ 的流是类型安全的 I/O 接口——`cout`/`cin` 替代 `printf`/`scanf`，自动处理类型匹配。

## 意图与场景

- 控制台输出（cout/cerr/clog）
- 控制台输入（cin）
- 类型安全的格式化输出

## 输出流

```cpp
#include <iostream>
#include <iomanip>

// 基本输出
std::cout << "Hello, " << 42 << " " << 3.14 << "\n";
std::cerr << "Error!\n";       // 不缓冲，立即输出
std::clog << "Log message\n";  // 可能缓冲

// 格式化
std::cout << std::hex << 255;           // "ff"
std::cout << std::oct << 10;            // "12"
std::cout << std::dec;                  // 恢复十进制
std::cout << std::fixed << std::setprecision(2) << 3.14159;  // "3.14"
std::cout << std::setw(10) << std::setfill('0') << 42;       // "0000000042"
std::cout << std::boolalpha << true;    // "true"
std::cout << std::left << std::setw(10) << "hi";  // "hi        "
```

## 输入流

```cpp
#include <iostream>
#include <string>

int n;
std::cin >> n;                    // 读取整数（跳过空白）

double d;
std::cin >> d;                    // 读取浮点数

std::string word;
std::cin >> word;                 // 读取单词（空格分隔）

// 读取整行
std::string line;
std::getline(std::cin, line);    // 读取一行（不含换行符）

// 流状态
if (std::cin.fail()) { }         // 输入类型不匹配
if (std::cin.eof()) { }          // 到达文件尾
std::cin.clear();                 // 清除错误状态
std::cin.ignore(1000, '\n');     // 丢弃最多1000个字符直到换行
```

## 自定义类型 IO

```cpp
struct Point {
    double x, y;
};

std::ostream& operator<<(std::ostream& os, const Point& p) {
    return os << "(" << p.x << ", " << p.y << ")";
}

std::istream& operator>>(std::istream& is, Point& p) {
    char lparen, comma, rparen;
    is >> lparen >> p.x >> comma >> p.y >> rparen;
    // 输入格式: (1.0, 2.0)
    return is;
}
```

## 关键要点

> `std::endl` 刷新缓冲区（性能代价），用 `'\n'` 代替除非需要立即刷新。`cerr` 默认无缓冲，适合错误输出。

> `>>` 运算符跳过空白。`getline` 读取整行包括空白。混用 `>>` 和 `getline` 时注意缓冲区中残留的换行符。

## 相关模式 / 关联

- [[cpp-运算符重载]] — `<<` 和 `>>` 的重载
- [[cpp-format]] — C++20 的现代替代
