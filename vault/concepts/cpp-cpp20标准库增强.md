---
title: C++20 标准库增强
tags: [cpp20, library, span, format, ranges, semaphore, jthread, source-location]
aliases: [C++20库, span, format, ranges, semaphore, jthread, source_location]
created: 2026-04-04
updated: 2026-04-04
---

# C++20 标准库增强

C++20 的库增强填补了许多长期空缺——`span`、`format`、`source_location` 等让日常编码更舒适。

## 主要新组件

```cpp
// std::span — 连续数据视图
void process(std::span<const int> data);
process(arr); process(vec); process(std_arr);  // 统一接口

// std::format — 类型安全格式化
std::string s = std::format("Hello, {}! Age: {}", name, age);

// std::source_location — 替代 __FILE__ / __LINE__
void log(std::string_view msg,
    std::source_location loc = std::source_location::current()) {
    std::cout << loc.file_name() << ":" << loc.line() << " " << msg;
}
log("something happened");  // 自动获取调用位置

// std::endian — 字节序查询
constexpr bool little = std::endian::native == std::endian::little;

// std::bit_cast — 类型双关（安全）
float f = 3.14f;
uint32_t bits = std::bit_cast<uint32_t>(f);  // 安全的位模式复制

// std::to_array — C 数组转 std::array
auto arr = std::to_array<int>({1, 2, 3, 4, 5});

// std::bind_front — 绑定前几个参数
auto add5 = std::bind_front(std::plus<>{}, 5);
add5(3);  // 8

// std::remove_cvref — 去掉 const/volatile/引用
using T = std::remove_cvref_t<const int&>;  // int

// std::midpoint — 中点（避免溢出）
int mid = std::midpoint(1, 100);  // 50

// std::lerp — 线性插值
double val = std::lerp(0.0, 10.0, 0.5);  // 5.0
```

## 协程相关

```cpp
// std::coroutine_handle — 协程句柄
// std::coroutine_traits — 协程特性
// std::suspend_always / std::suspend_never — 挂起策略
// （需要配套使用，见协程专题）
```

## 关键要点

> `source_location` 替代了宏 `__FILE__` 和 `__LINE__`——它是语言特性，更可靠。`bit_cast` 替代了不安全的 `reinterpret_cast` 类型双关。

## 相关模式 / 关联

- [[cpp-span]] — span 专题
- [[cpp-format]] — format 专题
- [[cpp-range库]] — ranges 专题
