---
title: Google Test 实战指南
tags: [cpp, testing, gtest, unit-test, assertion, fixture]
aliases: [GTest 使用, 单元测试框架, TEST/TEST_F]
created: 2026-04-05
updated: 2026-04-05
---

# Google Test 实战指南

**一句话概述：** Google Test（gtest）是 C++ 最流行的单元测试框架——TEST 定义测试用例、TEST_F 用 fixture 共享设置/清理、EXPECT_* 非致命断言、ASSERT_* 致命断言。死亡测试（EXPECT_DEATH）验证程序正确崩溃。

```cpp
#include <gtest/gtest.h>

// 基本测试
TEST(MathTest, Addition) {
    EXPECT_EQ(1 + 1, 2);
    EXPECT_NE(1 + 2, 4);
    EXPECT_NEAR(0.1 + 0.2, 0.3, 1e-9);
}

// Fixture：共享设置
class VectorTest : public ::testing::Test {
protected:
    void SetUp() override { v = {1, 2, 3, 4, 5}; }
    std::vector<int> v;
};

TEST_F(VectorTest, Size) { EXPECT_EQ(v.size(), 5); }
TEST_F(VectorTest, Sum) { EXPECT_EQ(std::accumulate(v.begin(), v.end(), 0), 15); }

// 参数化测试
class ParamTest : public ::testing::TestWithParam<int> {};
TEST_P(ParamTest, IsPositive) { EXPECT_GT(GetParam(), 0); }
INSTANTIATE_TEST_SUITE_P(Values, ParamTest, ::testing::Values(1, 2, 3));
```

## 关键要点

> 好的测试遵循 FIRST 原则：Fast（毫秒级）、Isolated（不依赖外部状态）、Repeatable（每次结果一致）、Self-validating（自动判断对错）、Timely（和代码一起写）。

## 相关模式 / 关联

- [[cpp-测试基础]] — 测试概览
- [[cpp-Mock与Stub]] — Mock 技术
- [[cpp-集成测试策略]] — 测试分层
