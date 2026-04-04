---
title: 文件流与字符串流
tags: [cpp, fstream, ifstream, ofstream, stringstream, istringstream]
aliases: [fstream, ifstream, ofstream, stringstream, 文件读写, 字符串流]
created: 2026-04-04
updated: 2026-04-04
---

# 文件流与字符串流

文件流做文件 I/O，字符串流做内存中的字符串格式化——两者都继承自 iostream 体系。

## 文件流

```cpp
#include <fstream>
#include <string>

// 写文件
std::ofstream out("output.txt");
if (!out) { /* 打开失败 */ }
out << "Hello, " << 42 << "\n";
out.close();  // 可选，析构时自动关闭

// 读文件
std::ifstream in("input.txt");
std::string line;
while (std::getline(in, line)) {
    std::cout << line << "\n";
}

// 读取整个文件
std::ifstream in2("data.txt");
std::ostringstream buffer;
buffer << in2.rdbuf();                    // 将文件内容读入字符串流
std::string content = buffer.str();

// 文件打开模式
std::ofstream app("log.txt", std::ios::app);     // 追加模式
std::fstream rw("data.bin", std::ios::in | std::ios::out | std::ios::binary);  // 二进制读写
```

## 字符串流

```cpp
#include <sstream>

// ostringstream：构建字符串
std::ostringstream oss;
oss << "Name: " << name << ", Age: " << age;
std::string result = oss.str();  // "Name: Alice, Age: 25"

// istringstream：解析字符串
std::istringstream iss("42 3.14 hello");
int n;
double d;
std::string s;
iss >> n >> d >> s;  // n=42, d=3.14, s="hello"

// 字符串分割
std::string data = "one,two,three,four";
std::istringstream ss(data);
std::string token;
while (std::getline(ss, token, ',')) {
    std::cout << token << "\n";
}
```

## 与 C 文件 IO 的对比

```cpp
// C 方式
FILE* fp = fopen("data.bin", "rb");
char buf[1024];
fread(buf, 1, 1024, fp);
fclose(fp);

// C++ 方式
std::ifstream in("data.bin", std::ios::binary);
char buf[1024];
in.read(buf, 1024);
// in.close();  // 析构自动关闭

// C++ 的优势：类型安全、RAII 自动关闭、异常安全
// C 的优势：某些边缘场景性能更好（二进制大文件读写）
```

## 关键要点

> 文件流对象在析构时自动关闭文件——不需要显式 `close()`。用 RAII 管理文件资源。

> `ostringstream` 是构建复杂字符串的首选方式（C++20 前），比字符串拼接高效。C++20 后 `std::format` 更简洁。

## 相关模式 / 关联

- [[cpp-流与IO基础]] — IO 流体系
- [[cpp-format]] — C++20 的格式化替代
