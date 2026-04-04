---
title: C++ 测试基础
tags: [cpp, testing, unit-test, Google-Test, assert, TDD]
aliases: [测试, 单元测试, Google Test, gtest, TDD, 测试框架]
created: 2026-04-04
updated: 2026-04-04
---

# C++ 测试基础

测试是代码质量的保证——Google Test 是 C++ 最流行的测试框架，`static_assert` 是编译期测试。

## Google Test 基础

```cpp
#include <gtest/gtest.h>

// TEST 宏：定义测试用例
TEST(MathTest, Addition) {
    EXPECT_EQ(1 + 1, 2);          // 期望相等（失败继续执行）
    ASSERT_EQ(2 + 2, 4);          // 断言相等（失败停止当前测试）
}

TEST(MathTest, Division) {
    EXPECT_DOUBLE_EQ(10.0 / 3.0, 3.3333333);  // 浮点比较
    EXPECT_THROW(divide(1, 0), std::runtime_error);  // 期望抛异常
    EXPECT_NO_THROW(divide(1, 1));  // 期望不抛异常
}

// 测试 fixture
class VectorTest : public ::testing::Test {
protected:
    std::vector<int> v;
    void SetUp() override { v = {1, 2, 3, 4, 5}; }
};

TEST_F(VectorTest, Size) {
    EXPECT_EQ(v.size(), 5);
}

TEST_F(VectorTest, PushBack) {
    v.push_back(6);
    EXPECT_EQ(v.size(), 6);
}
```

## 常用断言

```cpp
EXPECT_EQ(a, b);      // a == b
EXPECT_NE(a, b);      // a != b
EXPECT_LT(a, b);      // a < b
EXPECT_LE(a, b);      // a <= b
EXPECT_GT(a, b);      // a > b
EXPECT_GE(a, b);      // a >= b
EXPECT_TRUE(cond);    // cond 为 true
EXPECT_FALSE(cond);   // cond 为 false
EXPECT_STREQ(a, b);   // C 字符串相等
EXPECT_FLOAT_EQ(a, b);  // 浮点数相等（容差 4 ULP）
EXPECT_NEAR(a, b, tol);  // |a - b| <= tol
```

## 编译期测试

```cpp
// static_assert：编译期断言
static_assert(sizeof(int) == 4);
static_assert(std::is_integral_v<int>);
static_assert(std::is_same_v<int, int32_t>);

// 概念测试
template <typename T>
concept HasSize = requires(T t) { t.size(); };

static_assert(HasSize<std::vector<int>>);
static_assert(!HasSize<int>);
```

## 关键要点

> `EXPECT_*` 失败时继续测试，`ASSERT_*` 失败时停止当前测试。用 `EXPECT` 做常规检查，用 `ASSERT` 做前置条件检查。

> 测试应该独立、可重复、快速——每个测试用例不依赖其他测试的状态。

## 相关模式 / 关联

- [[cpp-调试技术与断言]] — assert 和 static_assert
- [[cpp-const与constexpr]] — 编译期测试
