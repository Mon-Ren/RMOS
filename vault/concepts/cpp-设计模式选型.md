---
title: 设计模式在 C++ 中的选型
tags: [cpp, design-pattern, selection, runtime-polymorphism, compile-time]
aliases: [设计模式选型, 运行时vs编译时, 多态选型, pattern selection]
created: 2026-04-04
updated: 2026-04-04
---

# 设计模式在 C++ 中的选型

C++ 独特地同时支持运行时多态（虚函数）和编译时多态（模板）——选择哪种决定了性能和灵活性的权衡。

## 多态选型

```
需要运行时改变行为？
├─ 是 → 运行时多态（虚函数、variant、function）
└─ 否 → 编译时多态（模板、constexpr、if constexpr）

性能关键？
├─ 是 → 编译时多态（零开销）
└─ 否 → 运行时多态（更灵活）

类型集合在编译期已知？
├─ 是 → variant + visit
└─ 否 → 虚函数继承层次
```

## 策略模式的三种实现

```cpp
// 1. 运行时策略（传统 OOP）
class SortStrategy {
public:
    virtual void sort(std::vector<int>&) = 0;
    virtual ~SortStrategy() = default;
};
class QuickSort : public SortStrategy { /* ... */ };
// 使用时通过指针切换策略

// 2. 编译时策略（模板参数）
template <typename SortPolicy>
class Container {
    SortPolicy policy_;
public:
    void sort(std::vector<int>& v) { policy_.sort(v); }
};
Container<QuickSortPolicy> c;  // 零开销

// 3. 函数对象策略（最灵活）
class Container2 {
    std::function<void(std::vector<int>&)> sorter_;
public:
    template <typename F>
    void set_sorter(F f) { sorter_ = std::move(f); }
};
```

## 选择指南

```
场景                              推荐方案
────────────────────────────────────────────
行为在运行时切换                  虚函数 / variant
行为在编译时确定                  模板参数 / CRTP
需要类型擦除                      std::function / any
回调简单                          Lambda
接口扩展                          组合而非继承
性能关键路径                      编译时多态
需要 ABI 达界                     虚函数（接口稳定）
```

## 关键要点

> C++ 的优势在于编译时多态——零运行时开销。优先考虑模板方案，只在真正需要运行时灵活性时用虚函数。

> variant + visit 是虚函数继承的替代——不需要堆分配，cache 更友好，但类型集合必须编译期已知。

## 相关模式 / 关联

- [[cpp-继承与多态]] — 运行时多态
- [[cpp-模板编程基础]] — 编译时多态
- [[cpp-variant]] — variant 的多态
