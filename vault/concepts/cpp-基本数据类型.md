---
title: C++ 基本数据类型
tags: [cpp, fundamentals, types, primitive]
aliases: [基本类型, primitive types, 内置类型, built-in types]
created: 2026-04-04
updated: 2026-04-04
---

# C++ 基本数据类型

C++ 提供一组固定宽度语义不固定的基本类型，实际大小依赖实现和平台，这是 C++ 兼容硬件多样性的代价。

## 意图与场景

- 需要精确控制内存占用时选择合适的基本类型
- 跨平台开发时必须理解类型大小的不确定性
- 性能敏感场景需要权衡类型宽度与硬件亲和性

## 类型体系

### 整数类型

```cpp
#include <cstddef>
#include <cstdint>

// 大小关系（典型 64 位平台）：
// char == signed char == unsigned char == 1 byte
// short <= int <= long <= long long

// 有符号与无符号
signed char sc = -128;        // 至少 8 位
unsigned char uc = 255;       // 至少 8 位，无符号
int i = 42;                   // 至少 16 位，通常 32 位
long l = 100L;                // 至少 32 位
long long ll = 1000LL;        // 至少 64 位

// 固定宽度类型（C++11，推荐跨平台使用）
int8_t   a = 0;               // 精确 8 位
int16_t  b = 0;               // 精确 16 位
int32_t  c = 0;               // 精确 32 位
int64_t  d = 0;               // 精确 64 位
uint32_t e = 0;               // 无符号 32 位
```

### 浮点类型

```cpp
float f = 3.14f;              // 通常 32 位，IEEE 754 单精度
double d = 3.14159265358979;  // 通常 64 位，IEEE 754 双精度
long double ld = 3.14L;       // 80/128 位，平台相关
```

### 字符类型

```cpp
char c = 'A';                 // 通常 8 位，符号性实现定义
wchar_t wc = L'A';            // 宽字符，平台相关大小
char8_t c8 = u8'A';           // C++20，UTF-8 编码单元
char16_t c16 = u'A';          // UTF-16 编码单元
char32_t c32 = U'A';          // UTF-32 编码单元
```

### 布尔类型

```cpp
bool flag = true;             // sizeof(bool) 实现定义，通常 1 字节
// 非零 → true，零 → false
// bool 隐式转换：true→1，false→0
```

### 特殊类型

```cpp
std::nullptr_t np = nullptr;  // C++11 空指针类型
std::byte b{0xFF};            // C++17 原始字节，不做算术
void* pv = nullptr;           // 通用指针，不能解引用
```

## sizeof 与平台差异

```cpp
#include <iostream>

int main() {
    // 典型 x86-64 Linux/Windows 输出：
    std::cout << sizeof(char)       << "\n";  // 1
    std::cout << sizeof(short)      << "\n";  // 2
    std::cout << sizeof(int)        << "\n";  // 4
    std::cout << sizeof(long)       << "\n";  // 4 (Windows) 或 8 (Linux)
    std::cout << sizeof(long long)  << "\n";  // 8
    std::cout << sizeof(float)      << "\n";  // 4
    std::cout << sizeof(double)     << "\n";  // 8
    std::cout << sizeof(void*)      << "\n";  // 8 (64位) 或 4 (32位)
}
```

## 整数提升与转换规则

```cpp
// 整数提升：小类型自动提升为 int（或 unsigned int）
char a = 100;
char b = 200;
auto c = a + b;  // c 是 int，值 300（不会溢出为 char）

// 有符号/无符号混合：无符号"吞噬"有符号
unsigned int u = 1;
int s = -1;
auto r = u + s;  // r 是 unsigned int，值为巨大的正数！
```

## 关键要点

> C++ 基本类型的大小是平台相关的，跨平台代码应使用 `<cstdint>` 中的固定宽度类型。

> 有符号与无符号混合运算会导致隐式转换，是经典的 bug 来源。

## 相关模式 / 关联

- [[cpp-类型转换]] — static_cast/reinterpret_cast 与基本类型
- [[cpp-auto-与类型推导]] — auto 对基本类型的行为
