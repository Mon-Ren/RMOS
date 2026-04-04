---
title: 随机数与分布
tags: [cpp, random, mt19937, distribution, uniform, engine]
aliases: [随机数, mt19937, 分布, uniform_int_distribution, 随机引擎]
created: 2026-04-04
updated: 2026-04-04
---

# 随机数与分布（C++11）

C++11 的 `<random>` 库将随机数引擎和分布分离——类型安全、高性能、可复现。

## 引擎 + 分布

```cpp
#include <random>

// 引擎：生成原始随机数
std::mt19937 rng(std::random_device{}());  // Mersenne Twister，种子来自硬件

// 分布：将原始随机数映射到目标范围
std::uniform_int_distribution<int> dice(1, 6);       // 1-6 均匀整数
std::uniform_real_distribution<double> unit(0.0, 1.0); // 0.0-1.0 均匀实数
std::normal_distribution<double> normal(0.0, 1.0);     // 正态分布
std::bernoulli_distribution coin(0.5);                 // 伯努利（硬币）

// 使用
int roll = dice(rng);         // 投骰子
double val = unit(rng);       // 0-1 随机实数
double z = normal(rng);       // 标准正态分布
bool heads = coin(rng);       // 硬币正面
```

## 常用分布

```cpp
std::uniform_int_distribution<int> d1(1, 100);     // 整数均匀 [1, 100]
std::uniform_real_distribution<double> d2(0, 1);   // 实数均匀 [0, 1)
std::normal_distribution<double> d3(50, 10);        // 正态 N(50, 10²)
std::exponential_distribution<double> d4(1.0);      // 指数分布
std::poisson_distribution<int> d5(4.0);             // 泊松分布 λ=4
std::bernoulli_distribution d6(0.7);                // 70% 概率 true
std::discrete_distribution<int> d7({10, 20, 70});   // 离散：10%选0, 20%选1, 70%选2
```

## 范围随机数

```cpp
// [min, max] 范围内的随机整数
int rand_int(int min, int max) {
    thread_local static std::mt19937 rng(std::random_device{}());
    std::uniform_int_distribution<int> dist(min, max);
    return dist(rng);
}

// 洗牌
std::vector<int> v = {1, 2, 3, 4, 5};
std::shuffle(v.begin(), v.end(), rng);

// 随机选择元素
auto it = std::next(v.begin(), std::uniform_int_distribution<int>(0, v.size()-1)(rng));
```

## 关键要点

> 引擎和分布分开是 C++ 随机数库的设计精髓——同一个引擎配合不同分布可以产生各种类型的随机数。

> `mt19937` 是最常用的引擎（周期 2^19937-1）。`random_device` 用于种子——不要用它直接生成随机数（可能很慢）。

## 相关模式 / 关联

- [[cpp-stl算法总览]] — shuffle 算法
- [[cpp-call_once与thread_local]] — thread_local 随机引擎
