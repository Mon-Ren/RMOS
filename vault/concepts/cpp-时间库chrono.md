---
title: C++ 标准库时间库
tags: [cpp, chrono, time, duration, time-point, clock]
aliases: [chrono, 时间库, duration, time_point, clock, 时间处理]
created: 2026-04-04
updated: 2026-04-04
---

# C++ 标准库时间库（chrono）

`<chrono>` 是 C++ 的时间库——类型安全的时间计算，避免整数单位混淆。

## 核心概念

```cpp
#include <chrono>
using namespace std::chrono_literals;

// duration：时间段
auto d1 = 100ms;              // milliseconds
auto d2 = 30s;                // seconds
auto d3 = 2min;               // minutes
auto d4 = 1h;                 // hours

// time_point：时间点
auto now = std::chrono::system_clock::now();
auto deadline = now + 5s;

// clock：时钟
// system_clock：系统时钟（可能调整，如 NTP）
// steady_clock：单调时钟（不后退，适合计时）
// high_resolution_clock：最高精度时钟
```

## 计时

```cpp
// 用 steady_clock 做精确计时
auto start = std::chrono::steady_clock::now();
// ... 操作 ...
auto end = std::chrono::steady_clock::now();
auto elapsed = end - start;
std::cout << std::chrono::duration_cast<std::chrono::microseconds>(elapsed).count() << "μs\n";

// sleep
std::this_thread::sleep_for(100ms);
std::this_thread::sleep_until(std::chrono::system_clock::now() + 1s);
```

## 时间计算

```cpp
auto duration = 2h + 30min + 15s;  // 类型安全的计算
auto ms = std::chrono::duration_cast<std::chrono::milliseconds>(duration);
std::cout << ms.count() << "ms\n";  // 9015000ms

// C++20: 日历和时区
auto today = std::chrono::year{2024} / std::chrono::month{1} / std::chrono::day{15};
auto tp = std::chrono::sys_days{today};  // 转为 time_point
```

## 关键要点

> 用 `steady_clock` 做计时（不受系统时间调整影响），用 `system_clock` 做日历时间。

> `duration_cast` 是显式的——防止精度丢失。`duration` 的隐式转换只允许扩大精度。

## 相关模式 / 关联

- [[cpp-performance分析]] — 计时
- [[cpp-自定义字面量]] — 时间字面量
