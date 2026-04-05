---
title: constexpr 分配与编译期容器
tags: [cpp20, constexpr, dynamic-allocation, compile-time-vector, compile-time-string]
aliases: [编译期动态分配, constexpr vector, 编译期容器]
created: 2026-04-05
updated: 2026-04-05
---

# constexpr 分配与编译期容器

**一句话概述：** C++20 允许在 constexpr 中使用 `new`/`delete` 和动态容器（`std::vector`、`std::string`）——但编译期分配的内存在编译结束时必须全部释放。这意味着你可以在编译期构建 vector、排序、过滤、做复杂的计算，只要最终结果不涉及悬垂指针。

## C++20 放开了什么

```
C++14：constexpr 函数可以有局部变量、循环、if，但不能有 try-catch
C++17：放宽了限制，但仍禁止虚函数、try-catch，不能用动态内存
C++20：
  ✅ new/delete（编译期）
  ✅ std::vector（编译期）
  ✅ std::string（编译期）
  ✅ 虚函数（编译期）
  ✅ try-catch（编译期）
  ✅ union 的非活动成员访问
  ❌ 静态变量、线程局部变量
  ❌ goto、volatile
  ❌ asm
```

## 编译期 vector

```cpp
#include <vector>
#include <algorithm>
#include <numeric>

constexpr std::vector<int> make_sorted_primes(int limit) {
    std::vector<int> primes;
    std::vector<bool> is_prime(limit + 1, true);
    is_prime[0] = is_prime[1] = false;

    for (int i = 2; i <= limit; ++i) {
        if (is_prime[i]) {
            primes.push_back(i);
            for (int j = i * 2; j <= limit; j += i) {
                is_prime[j] = false;
            }
            // 筛法
        }
    }

    // 编译期排序（为什么不行？）
    // 实际上 C++20 constexpr vector 已经支持大部分操作
    return primes;
}

// 编译期执行！
constexpr auto primes = make_sorted_primes(100);
// primes[0] == 2, primes[1] == 3, primes[2] == 5, ...

static_assert(primes[0] == 2);
static_assert(primes[1] == 3);
static_assert(primes[4] == 11);
static_assert(primes.size() == 25);  // 100 以内 25 个素数
```

## 编译期 string

```cpp
#include <string>
#include <algorithm>

constexpr std::string reverse_string(std::string s) {
    std::reverse(s.begin(), s.end());
    return s;
}

constexpr auto reversed = reverse_string("Hello, World!");
static_assert(reversed == "!dlroW ,olleH");

// 编译期字符串处理
constexpr std::string to_upper(std::string s) {
    for (char& c : s) {
        if (c >= 'a' && c <= 'z') {
            c = c - 'a' + 'A';
        }
    }
    return s;
}

constexpr auto upper = to_upper("hello world");
static_assert(upper == "HELLO WORLD");
```

## 编译期排序与搜索

```cpp
#include <vector>
#include <algorithm>

constexpr auto sorted_data() {
    std::vector<int> v = {5, 2, 8, 1, 9, 3, 7, 4, 6};
    std::sort(v.begin(), v.end());
    return v;
}

constexpr auto data = sorted_data();
static_assert(data[0] == 1);
static_assert(data[8] == 9);

// 二分查找
constexpr bool contains(const std::vector<int>& v, int target) {
    return std::binary_search(v.begin(), v.end(), target);
}

static_assert(contains(data, 5));   // true
static_assert(!contains(data, 10)); // false
```

## 编译期计算的实际应用

```cpp
// 场景：预计算查找表
#include <array>
#include <cmath>

constexpr auto make_sqrt_table() {
    std::array<double, 256> table{};
    for (int i = 0; i < 256; ++i) {
        // C++20 constexpr 不支持 std::sqrt，但可以用牛顿迭代
        double x = static_cast<double>(i);
        double guess = x / 2.0;
        for (int iter = 0; iter < 20; ++iter) {
            guess = (guess + x / guess) / 2.0;
        }
        table[i] = guess;
    }
    return table;
}

constexpr auto sqrt_table = make_sqrt_table();
// sqrt_table[25] == 5.0
// 整个表在编译期计算完成，运行时零开销

// 场景：编译期验证正则表达式（简化版）
constexpr bool is_valid_identifier(std::string_view s) {
    if (s.empty()) return false;
    if (!((s[0] >= 'a' && s[0] <= 'z') || (s[0] >= 'A' && s[0] <= 'Z') || s[0] == '_'))
        return false;
    for (char c : s.substr(1)) {
        if (!((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') ||
              (c >= '0' && c <= '9') || c == '_'))
            return false;
    }
    return true;
}

static_assert(is_valid_identifier("my_var_123"));
static_assert(!is_valid_identifier("123abc"));
static_assert(!is_valid_identifier(""));
```

## 编译期内存的限制

```cpp
// ❌ 编译期分配的内存不能泄漏
constexpr int* leak() {
    int* p = new int(42);
    return p;  // ❌ 返回了编译期分配的指针
    // 编译错误：编译期分配的内存在编译结束时必须释放
}

// ❌ 编译期分配的内存不能跨 constexpr 边界保存
constexpr auto make_vec() {
    std::vector<int> v = {1, 2, 3};
    return v;  // ✅ 返回值（移动语义）
    // 编译器会处理内部指针的转移
}

// ✅ 编译期内部使用，结束后释放
constexpr int compute() {
    std::vector<int> v;
    for (int i = 0; i < 100; ++i) v.push_back(i * i);
    int sum = 0;
    for (int x : v) sum += x;
    return sum;  // v 在函数结束时析构，内存释放
}

static_assert(compute() == 328350);  // 0² + 1² + ... + 99²
```

## 关键要点

> `constexpr std::vector` 和 `constexpr std::string` 在编译期的行为和运行时一致——可以 push_back、insert、erase、sort 等。唯一的限制是编译结束时所有内存必须释放。

> 编译期 `new`/`delete` 的实现方式：编译器在编译时维护一个虚拟内存空间，所有 constexpr new 在其中分配，constexpr delete 回收。编译结束时检查是否有未释放的内存——有则编译错误。

> 实际收益：(1) 编译期验证更复杂的条件，(2) 预计算查找表（零运行时开销），(3) 编译期构建数据结构。但编译时间会增加——复杂的 constexpr 计算可能让编译时间翻倍。

## 相关模式 / 关联

- [[cpp-编译期计算与constexpr深入]] — constexpr 演进全貌
- [[cpp-consteval与constinit区别]] — consteval 强制编译期
- [[cpp-编译期字符串处理]] — 编译期字符串操作
- [[cpp-编译期校验与static_assert]] — 编译期断言
- [[cpp-vector深入]] — 运行时 vector 的更多细节
