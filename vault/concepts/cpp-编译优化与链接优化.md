---
title: 编译优化与链接优化
tags: [cpp, optimization, compiler, LTO, PGO, inline, constexpr]
aliases: [编译优化, LTO, PGO, 链接时优化, profile-guided, 编译器优化]
created: 2026-04-04
updated: 2026-04-04
---

# 编译优化与链接优化

编译器优化让相同代码跑得更快——理解优化选项和限制条件能帮助写出更易优化的代码。

## 编译器优化级别

```bash
g++ -O0 main.cpp    # 无优化（调试默认）：编译快，代码慢
g++ -O1 main.cpp    # 基本优化
g++ -O2 main.cpp    # 标准优化（发布推荐）：大部分场景最佳
g++ -O3 main.cpp    # 激进优化：可能增大代码体积
g++ -Os main.cpp    # 优化体积
g++ -Og main.cpp    # 调试友好的优化
g++ -Ofast main.cpp # O3 + 放松标准合规（可能改变数学结果）
```

## 内联

```cpp
// inline 关键字的现代含义：
// 1. 允许在多个翻译单元中定义（替代 static）
// 2. 建议编译器内联（编译器可忽略）

inline int square(int x) { return x * x; }

// 编译器自动内联：
// - 短小的函数（即使没标 inline）
// - 构造函数、析构函数中的简单操作
// - lambda 表达式
// - 模板实例化后的函数

// 强制内联（非标准但广泛支持）
__attribute__((always_inline)) int fast_add(int a, int b) { return a + b; }
__forceinline int fast_add(int a, int b) { return a + b; }  // MSVC
```

## LTO（Link-Time Optimization）

```bash
# 编译时：
g++ -flto -O2 -c a.cpp -o a.o
g++ -flto -O2 -c b.cpp -o b.o

# 链接时（LTO 在此阶段执行跨文件优化）：
g++ -flto -O2 a.o b.o -o program

# LTO 的效果：
# - 跨文件内联
# - 跨文件消除未使用的代码
# - 跨文件常量传播
# 编译时间变长，但运行更快
```

## PGO（Profile-Guided Optimization）

```bash
# 第一步：插桩编译
g++ -fprofile-generate -O2 main.cpp -o program

# 第二步：运行收集数据
./program  # 用代表性工作负载运行

# 第三步：用数据优化编译
g++ -fprofile-use -O2 main.cpp -o program

# PGO 的效果：
# - 基于实际数据的分支概率
# - 热路径优化、冷路径布局
# - 更准确的内联决策
```

## 代码层面帮助编译器优化

```cpp
// 1. constexpr：编译期计算，零运行时开销
constexpr int factorial(int n) { /* ... */ }

// 2. const：告诉编译器值不变，可做更多优化
void process(const int* data, size_t n);

// 3. restrict（C++ 无标准支持，用 __restrict）
void add(float* __restrict a, const float* __restrict b, size_t n);

// 4. 分支预测提示
if (likely_condition) [[likely]] { /* ... */ }

// 5. 避免虚函数（虚函数阻止内联）
// 6. 减少间接调用（函数指针、std::function）
// 7. 数据连续（vector 优于 list）
```

## 关键要点

> `-O2` 是发布构建的默认选择。LTO 在链接阶段做跨文件优化，对大型项目收益显著。PGO 用实际运行数据指导优化。

> `inline` 的主要现代含义是"允许多定义"而非"强制内联"——编译器在 `-O2` 下自动内联比手动标记更聪明。

## 相关模式 / 关联

- [[cpp-const与constexpr]] — 编译期计算
- [[cpp-内联函数]] — 内联深入
