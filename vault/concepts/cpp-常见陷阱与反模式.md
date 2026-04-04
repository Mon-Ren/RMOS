---
title: C++ 常见陷阱与反模式
tags: [cpp, pitfalls, anti-pattern, common-mistakes, bugs]
aliases: [常见陷阱, 反模式, 常见错误, bugs, 最常见bug]
created: 2026-04-04
updated: 2026-04-04
---

# C++ 常见陷阱与反模式

这些是 C++ 社区总结的最常见错误——了解它们能避免大量调试时间。

## 最常见陷阱

```cpp
// 1. vector<bool> 的代理对象
std::vector<bool> flags = {true, false};
auto flag = flags[0];  // flag 不是 bool&，是代理对象的拷贝！
// 修改 flag 不会影响 flags[0]
// 用 std::vector<int> 或 std::bitset 替代

// 2. string 的引用失效
std::string s = "hello";
const char* p = s.c_str();
s += " world";  // 可能重新分配，p 悬垂！

// 3. map::operator[] 插入默认值
std::map<std::string, int> m;
int val = m["missing"];  // 插入了 {"missing", 0}！
// 用 m.find() 或 m.at() 替代

// 4. 有符号/无符号比较
int i = -1;
unsigned u = 1;
if (i < u) { /* false！-1 转为巨大的 unsigned 值 */ }

// 5. auto 去掉了 const 和引用
const std::string& ref = get_string();
auto copy = ref;  // copy 是 string，不是 const string&

// 6. 构造函数初始化顺序
class Foo {
    int b_, a_;
    Foo(int x) : a_(x), b_(a_) {}  // b_ 先于 a_ 声明，b_ 用未初始化的 a_
};

// 7. delete this
// 在成员函数中 delete this 会导致之后访问成员 UB

// 8. 跨 DLL 边界传递 STL 容器
// 不同 DLL 可能有不同的堆 → 内存错误
```

## 反模式

```
❌ 继承代替组合          → 用组合，除非真正的 is-a
❌ 过度使用 shared_ptr    → 默认 unique_ptr
❌ 全局变量               → 用依赖注入或单例模式
❌ 滥用异常做流程控制     → 用返回值/optional
❌ 过早优化               → 先写对，再测量，再优化
❌ 复制粘贴代码           → 提取函数/模板
```

## 关键要点

> 大部分 C++ 陷阱来自隐式行为：隐式转换、隐式拷贝、隐式插入。现代 C++ 的 `explicit`、`enum class`、`string_view` 等特性减少了隐式行为。

## 相关模式 / 关联

- [[cpp-代码审查清单]] — 审查检查点
- [[cpp-悬垂指针与use-after-free]] — 常见内存错误
