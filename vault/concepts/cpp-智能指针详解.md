---
title: 智能指针详解
tags: [cpp, idiom, smart-pointer, memory-management]
aliases: [Smart Pointer, 智能指针, unique_ptr, shared_ptr, weak_ptr]
created: 2026-04-04
updated: 2026-04-04
---

# 智能指针详解

**一句话概述：** 用 RAII 管理动态内存——`unique_ptr` 独占所有权、`shared_ptr` 共享所有权（引用计数）、`weak_ptr` 打破循环引用，彻底告别手动 `new/delete`。

## 意图与场景

智能指针将内存管理自动化：

- **`unique_ptr`**：独占所有权，零开销抽象（和裸指针一样快）
- **`shared_ptr`**：共享所有权，引用计数（线程安全的控制块）
- **`weak_ptr`**：观察 `shared_ptr` 所管理的对象，不增加引用计数

**核心原则：默认用 `unique_ptr`，需要共享时才用 `shared_ptr`。**

## C++ 实现代码

### unique_ptr：独占所有权

```cpp
#include <memory>
#include <vector>
#include <iostream>
#include <cstdio>

// 基本用法
void unique_ptr_basics() {
    // 推荐：make_unique（C++14）
    auto p1 = std::make_unique<int>(42);
    auto p2 = std::make_unique<std::vector<int>>(10, 0);
    
    // 自定义删除器
    auto file = std::unique_ptr<std::FILE, decltype(&std::fclose)>(
        std::fopen("data.txt", "r"), &std::fclose);
    
    // 自定义删除器（lambda，需要额外模板参数）
    auto deleter = [](int* p) { std::cout << "deleting\n"; delete p; };
    std::unique_ptr<int, decltype(deleter)> p3(new int(10), deleter);
    
    // 移动所有权
    auto owner = std::make_unique<std::string>("hello");
    // auto copy = owner;           // ❌ 编译错误：不可拷贝
    auto new_owner = std::move(owner); // ✅ 转移所有权
    // owner 现在是 nullptr
    
    // 放入容器
    std::vector<std::unique_ptr<int>> vec;
    vec.push_back(std::make_unique<int>(1));
    vec.push_back(std::make_unique<int>(2));
}
```

### shared_ptr：共享所有权

```cpp
#include <memory>

void shared_ptr_basics() {
    // make_shared：一次分配对象+控制块（更高效）
    auto sp1 = std::make_shared<int>(42);
    
    {
        auto sp2 = sp1;  // 共享，引用计数 +1
        std::cout << "use_count: " << sp1.use_count() << "\n"; // 2
    }  // sp2 离开作用域，引用计数 -1
    
    std::cout << "use_count: " << sp1.use_count() << "\n"; // 1
    
    // 共享所有权场景
    struct Node {
        std::vector<std::shared_ptr<Node>> children;
        std::string name;
        Node(std::string n) : name(std::move(n)) {}
    };
    
    auto root = std::make_shared<Node>("root");
    auto child = std::make_shared<Node>("child");
    root->children.push_back(child);
    // root 和其他地方都可能持有 child
}
```

### weak_ptr：打破循环引用

```cpp
#include <memory>

// ❌ 循环引用导致内存泄漏
struct BadNode {
    std::shared_ptr<BadNode> next;
    ~BadNode() { std::cout << "BadNode destroyed\n"; }
};

void bad_example() {
    auto a = std::make_shared<BadNode>();
    auto b = std::make_shared<BadNode>();
    a->next = b;
    b->next = a;  // 循环引用！引用计数永远不为 0
}  // a 和 b 都不会被销毁 → 泄漏

// ✅ 用 weak_ptr 打破循环
struct GoodNode {
    std::weak_ptr<GoodNode> next;  // 不增加引用计数
    ~GoodNode() { std::cout << "GoodNode destroyed\n"; }
};

void good_example() {
    auto a = std::make_shared<GoodNode>();
    auto b = std::make_shared<GoodNode>();
    a->next = b;
    b->next = a;  // weak_ptr 不增加引用计数
}  // 正确销毁

// weak_ptr 安全使用
void use_weak_ptr() {
    std::weak_ptr<int> wp;
    {
        auto sp = std::make_shared<int>(42);
        wp = sp;
        
        // 检查对象是否还存活
        if (auto locked = wp.lock()) {  // lock() 返回 shared_ptr
            std::cout << "Value: " << *locked << "\n";
        }
    }
    // sp 销毁，对象已释放
    if (wp.expired()) {
        std::cout << "Object has been destroyed\n";
    }
}
```

### make_unique vs make_shared

```cpp
#include <memory>

void make_comparison() {
    // make_unique：简单封装 new
    // 一次堆分配（对象本身）
    auto up = std::make_unique<std::string>("hello");
    
    // make_shared：更高效但有限制
    // 一次堆分配（对象 + 控制块连续存储）
    auto sp = std::make_shared<std::string>("hello");
    
    // make_shared 的限制：
    // 1. 不能指定自定义删除器
    // 2. 对象内存直到最后一个 weak_ptr 销毁才释放
    //    （因为对象和控制块在同一块内存中）
    
    // 当需要自定义删除器时，必须用 shared_ptr 构造函数
    std::shared_ptr<int> raw(new int[10], [](int* p) { delete[] p; });
    // 注意：make_shared 不支持数组（C++17 起支持 make_shared<T[]>）
}
```

### 选择指南

```cpp
// 什么时候用哪个？
// 
// unique_ptr（默认选择）：
//   - 单一所有者
//   - 工厂函数返回值
//   - pimpl 模式
//   - POCO（Plain Old Container Ownership）
//
// shared_ptr：
//   - 多个所有者需要共享资源
//   - 缓存场景
//   - 异步回调需要延长对象生命周期
//
// weak_ptr：
//   - 观察者模式（不阻止被观察者销毁）
//   - 打破循环引用
//   - 缓存（检查对象是否仍存在）
//
// 裸指针/引用：
//   - 非所有权的观察和传递
//   - 不管理生命周期
```

## 优缺点

| 优点 | 缺点 |
|------|------|
| 自动内存管理，无泄漏 | shared_ptr 控制块有开销 |
| 异常安全 | 引用计数增加/减少有原子操作开销 |
| 所有权语义清晰 | 循环引用导致泄漏（需 weak_ptr） |
| unique_ptr 零开销 | make_shared 延长 weak_ptr 持有的内存 |

> [!tip] 关键要点
> **默认选择 `unique_ptr`**——它是零开销抽象，和裸指针一样快。只在确实需要共享所有权时才用 `shared_ptr`。永远用 `make_unique` / `make_shared` 而不是 `new`。裸指针仅用于**非所有权**的观察和传递。

> [!warning] 常见陷阱
> 1. `shared_ptr` 的原子引用计数比 `unique_ptr` 慢 ~2x
> 2. 不要用两个独立的 `shared_ptr` 管理同一裸指针（会 double-free）
> 3. `make_shared` 分配的内存直到所有 `weak_ptr` 销毁才释放
> 4. `shared_ptr` 的自定义删除器不参与类型（类型擦除），`unique_ptr` 的删除器参与类型

## 相关链接

- [[cpp-raii-惯用法]] — 智能指针是 RAII 的最经典应用
- [[cpp-移动语义]] — unique_ptr 依赖移动语义转移所有权
- [[代理模式]] — 智能指针可视为代理模式
- [[cpp-pimpl-惯用法]] — 内部使用 unique_ptr
