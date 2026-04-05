---
title: shared_ptr 控制块揭秘
tags: [cpp, smart-pointer, shared-ptr, control-block, make-shared]
aliases: [shared_ptr 内部实现, 控制块结构, make_shared 原理]
created: 2026-04-05
updated: 2026-04-05
---

# shared_ptr 控制块揭秘

**一句话概述：** `shared_ptr` 内部有一个"控制块"管理引用计数——`make_shared` 把对象和控制块合并为一次堆分配（更快、更缓存友好），但当 `weak_ptr` 存活时整块内存无法释放（对象析构但内存不归还）。

## 控制块结构

```
make_shared<T>(args...)
┌──────────────────────────────────────┐
│ 一次堆分配（单个内存块）               │
│ ┌──────────────────────────────────┐ │
│ │ 控制块                            │ │
│ │   ├── 强引用计数 (atomic<long>)    │ │
│ │   ├── 弱引用计数 (atomic<long>)    │ │
│ │   ├── 虚表指针（自定义删除器等）    │ │
│ │   └── aligned_storage for T       │ │ ← 对齐后的对象存储
│ │       T 对象就构造在这里           │ │
│ └──────────────────────────────────┘ │
└──────────────────────────────────────┘

shared_ptr<T>(new T(args...))
┌──────────────┐     ┌──────────────────┐
│ T 对象（堆）   │     │ 控制块（堆）       │
│              │     │   强引用计数       │
│              │     │   弱引用计数       │
└──────────────┘     │   删除器指针       │     ← 两个独立的堆分配
        ↑            │   指向 T 的指针 ────┼──→  T 对象
        │            └──────────────────┘
  shared_ptr 内部指针（sptr）
  指向 T 对象
```

## make_shared 的优势与陷阱

### 优势

```cpp
// 方式 A：两次堆分配
auto sp1 = std::shared_ptr<Widget>(new Widget());  // 分配 Widget + 分配控制块

// 方式 B：一次堆分配
auto sp2 = std::make_shared<Widget>();             // 只分配一次

// 性能差异：
// - make_shared 减少一次 malloc 调用（malloc 本身有锁开销）
// - 对象和引用计数在同一缓存行，访问更高效
// - 减少内存碎片
```

### 陷阱：weak_ptr 导致内存延迟释放

```cpp
std::weak_ptr<Widget> weak;

{
    auto sp = std::make_shared<Widget>();  // 分配整块内存
    weak = sp;                              // 弱引用 +1
}   // sp 析构 → 强引用为 0 → Widget 析构函数调用
    // 但！弱引用为 1 → 整块内存不释放
    // Widget 的"尸体"（已析构但未释放的内存）还在

weak.reset();  // 弱引用为 0 → 现在整块内存才释放
```

**为什么？** 因为 `make_shared` 把对象和控制块合并了。控制块必须活着（因为有 `weak_ptr` 指向它），控制块活着就意味着整块内存都活着——包括对象原来占的那部分。

**解决：** 如果对象很大且 `weak_ptr` 生命周期可能很长，用 `shared_ptr<T>(new T())` 替代 `make_shared`，这样对象析构后内存就能归还，控制块单独保留。

## 控制块何时创建

| 创建方式 | 控制块 |
|----------|--------|
| `make_shared<T>()` | 和 T 一起分配 |
| `shared_ptr<T>(new T())` | 独立分配 |
| `shared_ptr<T>(p, deleter)` | 独立分配 |
| `shared_ptr<T>(unique_ptr)` | 独立分配 |
| `shared_ptr<T>(weak_ptr)` | 已有控制块 |

**关键规则：** 每个由裸指针构造的 `shared_ptr` 都会创建新控制块。

```cpp
Widget* raw = new Widget();
std::shared_ptr<Widget> sp1(raw);   // 控制块 A
std::shared_ptr<Widget> sp2(raw);   // 控制块 B（独立的！）
// sp1 和 sp2 各自认为自己独占 raw → double delete → 崩溃
```

## 自定义删除器与控制块

```cpp
// 自定义删除器会被存储在控制块里（通过类型擦除）
auto sp = std::shared_ptr<FILE>(fopen("test.txt", "r"), [](FILE* f) {
    if (f) fclose(f);
});

// 控制块布局：
// ┌──────────────────┐
// │ 强引用计数         │
// │ 弱引用计数         │
// │ 删除器 lambda      │ ← 类型擦除存储
// │ deleter_size=16   │
// └──────────────────┘
```

不同的删除器类型不影响 `shared_ptr` 的类型——这是类型擦除的代价（虚调用）。

## 关键要点

> `enable_shared_from_this` 的原理：`shared_ptr` 构造时会检查 T 是否继承自 `enable_shared_from_this<T>`，如果是，就把控制块指针存到基类的 `weak_ptr` 里。这样 `shared_from_this()` 就能从 `this` 安全地构造 `shared_ptr`。

> 多线程下引用计数的原子操作是 `shared_ptr` 的主要开销。拷贝 `shared_ptr` 需要对强引用计数做 atomic increment（acquire-release），析构需要 atomic decrement（release）+ 如果归零则调用删除器。在高频拷贝/析构场景，这个开销可能显著。

> 循环引用：`shared_ptr` A 持有 B，B 持有 A → 引用计数永远不会归零 → 内存泄漏。解决：其中一个方向改用 `weak_ptr`。

## 相关模式 / 关联

- [[cpp-智能指针详解]] — unique_ptr/shared_ptr/weak_ptr 完整指南
- [[cpp-智能指针对比与最佳实践]] — 选择指南
- [[cpp-类型擦除]] — 删除器的类型擦除
- [[cpp-new与delete深入]] — 堆分配原理
- [[cpp-Rule-of-Zero与Rule-of-Five]] — 资源管理法则
