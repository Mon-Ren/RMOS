---
title: 调试技术与断言
tags: [cpp, debug, assert, static_assert, sanitizer, gdb, address-sanitizer]
aliases: [调试, assert, static_assert, sanitizer, ASan, UBSan, 调试技术]
created: 2026-04-04
updated: 2026-04-04
---

# 调试技术与断言

断言和 Sanitizer 是在开发阶段捕获 bug 的利器——assert 做运行时检查，static_assert 做编译期检查，Sanitizer 做内存/并发检查。

## assert 与 static_assert

```cpp
#include <cassert>

// 运行时断言：条件为 false 时终止
assert(ptr != nullptr);        // Release 模式通常被编译掉
assert(index < size());        // 调试阶段捕获越界

// static_assert：编译期断言
static_assert(sizeof(int) == 4, "int must be 4 bytes");
static_assert(std::is_integral_v<T>, "T must be integral");
// 不产生运行时开销，编译失败就是编译错误

// 自定义 assert
#define MY_ASSERT(cond, msg) \
    do { \
        if (!(cond)) { \
            std::cerr << "Assertion failed: " << msg << "\n"; \
            std::abort(); \
        } \
    } while(0)
```

## Sanitizer

```bash
# AddressSanitizer（ASan）：检测内存错误
g++ -fsanitize=address -g main.cpp -o main
./main  # 运行时检测：越界、use-after-free、double-free

# UndefinedBehaviorSanitizer（UBSan）：检测 UB
g++ -fsanitize=undefined -g main.cpp -o main
# 检测：整数溢出、空指针解引用、对齐错误

# ThreadSanitizer（TSan）：检测数据竞争
g++ -fsanitize=thread -g main.cpp -o main
# 检测：数据竞争、死锁

# MemorySanitizer（MSan）：检测未初始化读
g++ -fsanitize=memory -g main.cpp -o main
```

## 实用调试技巧

```cpp
// 条件断点等效
void debug_break() {
#ifdef _MSC_VER
    __debugbreak();
#else
    __builtin_trap();
#endif
}

// 格式化调试输出
#ifdef DEBUG
#define DBG(x) std::cerr << #x << " = " << (x) << "\n"
#else
#define DBG(x)
#endif

// 检查返回值
#define CHECK(expr) \
    do { if (!(expr)) { \
        std::cerr << "CHECK failed: " #expr " at " << __FILE__ << ":" << __LINE__; \
        std::abort(); \
    }} while(0)
```

## 关键要点

> 开发阶段始终开启 ASan 和 UBSan——它们用很小的性能代价捕获大量内存和 UB 问题。

> `static_assert` 零开销编译期检查——用于验证类型特征、大小假设等编译期不变量。

## 相关模式 / 关联

- [[cpp-const与constexpr]] — static_assert 依赖编译期常量
- [[cpp-异常处理]] — 运行时错误处理
