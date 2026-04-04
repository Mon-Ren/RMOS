---
title: 异常处理性能开销
tags: [cpp, exception, performance, overhead, zero-cost, table-based]
aliases: [异常性能, 异常开销, zero-cost exception, table-based, 异常机制]
created: 2026-04-04
updated: 2026-04-04
---

# 异常处理性能开销

C++ 异常的设计哲学是"不抛异常时零开销"——但抛异常时开销很大。理解这个权衡才能做出正确选择。

## 零开销模型

```
C++ 异常采用 table-based 方案（Itanium ABI）：

不抛异常时：
- 无运行时开销（不像返回码那样每步都检查）
- 额外的只读数据（异常表，存储在二进制文件中）
- 代码体积略有增加

抛异常时：
- 遍历调用栈（unwind）
- 查找异常表
- 运行局部对象的析构函数
- 比正常返回慢 100-1000 倍
```

## 实际测量

```cpp
// 正常路径 vs 异常路径的性能对比
void with_exception(int n) {
    try {
        if (n < 0) throw std::runtime_error("negative");
        // 正常处理（零异常开销）
    } catch (...) { }
}

void with_error_code(int n) {
    if (n < 0) { return; /* 错误处理 */ }
    // 正常处理（每步需检查返回码）
}

// 结论：
// - 正常路径：异常版本略快（不用检查返回码）
// - 异常路径：异常版本慢得多
// - 异常抛出频率 < 0.1% 时，异常总体性能更优
```

## 编译选项影响

```bash
# -fno-exceptions：禁用异常
# 优点：二进制体积小，性能可能略好
# 缺点：不能用 std::vector 等标准库

# -fexceptions：启用异常（默认）
# 标准库行为正常

# -DCMAKE_CXX_FLAGS="-fno-exceptions" 配合自定义错误处理
```

## 关键要点

> C++ 异常在不抛出时零开销——这是它与返回码方案的核心差异。只在真正的异常情况下（<1%概率）才抛异常。

> 如果代码频繁抛异常（如用异常做流程控制），性能会灾难性地下降——这绝对不该发生。

## 相关模式 / 关联

- [[cpp-异常处理]] — 异常的使用
- [[cpp-异常vs错误码]] — 选择指南
