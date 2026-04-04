---
title: C++ 代码规范与最佳实践
tags: [cpp, best-practices, coding-standard, guidelines, core-guidelines]
aliases: [代码规范, best practices, Core Guidelines, 编码标准, C++规范]
created: 2026-04-04
updated: 2026-04-04
---

# C++ 代码规范与最佳实践

基于 C++ Core Guidelines 的现代 C++ 编码规范——让代码更安全、更清晰、更高效。

## 命名规范

```cpp
// 类型名：PascalCase
class ThreadPool {};
struct ConnectionInfo {};
enum class LogLevel {};

// 函数/变量名：snake_case
void process_data();
int element_count;
std::string user_name;

// 常量：k 前缀 或 UPPER_CASE
constexpr int kMaxRetries = 3;
constexpr size_t BUFFER_SIZE = 1024;

// 私有成员：尾部下划线
class Widget {
    int value_;
    std::string name_;
};

// 宏：UPPER_CASE
#define ENABLE_DEBUG
```

## 类型选择

```
默认整数     → int（除非需要更大范围）
索引/大小    → size_t（无符号）
小整数       → int8_t/int16_t（需精确大小时）
浮点         → double（除非有 float 特殊需求）
字符串       → std::string（输入参数用 string_view）
固定数组     → std::array
动态数组     → std::vector
键值对       → std::unordered_map（默认）或 std::map（需有序）
可选值       → std::optional
多返回值     → 结构化绑定 / 结构体
```

## 接口设计

```cpp
// ✅ 不修改的参数用 const 引用
void process(const std::string& name);

// ✅ 输出参数用指针（明确表示会被修改）
void compute(int input, int* output);

// ✅ 需要转移所有权时显式用 unique_ptr
void take_ownership(std::unique_ptr<Widget> w);

// ✅ 不拥有资源时用裸指针或引用
void observe(Widget* w);      // 可以为 null
void observe(Widget& w);      // 不为 null

// ❌ 不要用 const unique_ptr&
void bad(const std::unique_ptr<Widget>& w);  // 用 Widget& 代替
```

## 内存与资源

```cpp
// ✅ 用 RAII 管理所有资源
auto file = std::make_unique<FileHandle>("data.txt");
std::lock_guard<std::mutex> lock(mtx);

// ✅ 用 make_unique/make_shared 创建对象
auto p = std::make_unique<Widget>(args);

// ❌ 避免裸 new/delete
Widget* p = new Widget();  // 谁负责 delete？

// ✅ 用 span/string_view 做非拥有视图
void process(std::span<const int> data);
```

## 关键要点

> 遵循 C++ Core Guidelines（isocpp.github.io/CppCoreGuidelines）——它是 Bjarne Stroustrup 和 Herb Sutter 维护的权威指南。

> 好的 C++ 代码：RAII 管理资源、const 尽量多用、接口意图明确、避免裸指针做所有权。

## 相关模式 / 关联

- [[cpp-Rule-of-Zero与Rule-of-Five]] — 特殊成员函数
- [[cpp-const正确性]] — const 的使用
