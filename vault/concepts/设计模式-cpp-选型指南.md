---
title: C++ 设计模式选型指南
tags: [cpp, design-pattern, guide, modern-cpp]
aliases: [C++ 模式选型, 模式选择指南, 运行时 vs 编译时多态, pattern selection]
created: 2026-04-04
updated: 2026-04-04
---

# C++ 设计模式选型指南

**一句话概述：** 面对具体问题时，如何在运行时多态（虚函数）与编译时多态（模板）之间选择，以及现代 C++ 特性如何替代经典 GoF 模式。

## 核心决策：运行时 vs 编译时

```
是否需要在运行时切换行为？
├── 是 → 运行时多态
│   ├── 简单接口 → 虚函数 / std::function
│   ├── 多个实现 → 抽象基类 + 工厂
│   └── 插件架构 → 动态库 + 类型擦除
└── 否 → 编译时多态
    ├── 需要性能 → CRTP / if constexpr
    ├── 策略组合 → Policy-Based Design
    └── 接口约束 → Concepts (C++20)
```

## 常见场景 → 推荐模式映射表

| 场景 | 推荐模式 | 现代 C++ 替代 |
|------|----------|--------------|
| 单一所有者管理资源 | RAII + `unique_ptr` | — |
| 需要共享资源 | `shared_ptr` | — |
| 隐藏实现细节 | Pimpl 惯用法 | 模块 (C++20) |
| 编译时接口检查 | CRTP | Concepts (C++20) |
| 运行时策略切换 | 策略模式 + 虚函数 | `std::function` |
| 编译时策略组合 | Policy-Based Design | Concepts + 模板 |
| 前置/后置钩子 | NVI（非虚接口） | — |
| 清理资源 | RAII | Scope Guard |
| 延迟求值 | Expression Templates | Ranges (C++20) |
| 类型安全的 void* | 类型擦除 | `std::any`, `std::function` |
| 编译期分支 | Tag Dispatch | `if constexpr` |
| 模板约束 | SFINAE | Concepts (C++20) |
| 回调/事件 | `std::function` | Lambda |
| 数据流处理 | — | Ranges (C++20) |
| 对象创建控制 | 工厂模式 | `std::make_unique` |
| 观察者通知 | Observer 模式 | `std::function` 回调 |
| 不可变数据 | — | `const` + 值语义 |

## 现代 C++ 特性对经典模式的替代

### 被取代或简化的模式

```cpp
// 1. Iterator 模式 → 内置支持
// 经典：实现 begin()/end()/operator++/operator*/operator==
// 现代：大多用 ranges + 迭代器即可

// 2. Visitor 模式 → std::variant + std::visit
#include <variant>
#include <string>

using Value = std::variant<int, double, std::string>;
void process(const Value& v) {
    std::visit([](const auto& val) {
        using T = std::decay_t<decltype(val)>;
        if constexpr (std::is_same_v<T, int>)
            std::cout << "int: " << val;
        else if constexpr (std::is_same_v<T, double>)
            std::cout << "double: " << val;
        else
            std::cout << "string: " << val;
    }, v);
}

// 3. Strategy 模式 → std::function
#include <functional>
class Sorter {
    std::function<bool(int, int)> comparator_;
public:
    void set_strategy(std::function<bool(int, int)> cmp) {
        comparator_ = std::move(cmp);
    }
};

// 4. Command 模式 → Lambda + std::function
#include <queue>
class CommandQueue {
    std::queue<std::function<void()>> queue_;
public:
    void enqueue(std::function<void()> cmd) { queue_.push(std::move(cmd)); }
    void execute_all() { while (!queue_.empty()) { queue_.front()(); queue_.pop(); } }
};

// 5. Factory 模式 → make_unique + 工厂函数
template <typename T, typename... Args>
std::unique_ptr<T> create(Args&&... args) {
    return std::make_unique<T>(std::forward<Args>(args)...);
}
```

### 仍然有价值的经典模式

```cpp
// 以下模式在现代 C++ 中仍然不可替代：

// 1. RAII —— 始终是资源管理的核心
// 2. Pimpl —— 库开发的编译防火墙
// 3. NVI —— 虚函数的前后置控制
// 4. Observer —— 事件系统仍然需要设计
// 5. Composite —— 树形结构 UI/文档模型
// 6. Proxy —— 延迟加载、访问控制
```

## 性能 vs 灵活性权衡

```cpp
// 决策矩阵：

// | 方式              | 灵活性 | 性能 | 编译时 | 运行时 |
// |-------------------|--------|------|--------|--------|
// | 虚函数            | 高     | 中   | ✗      | ✓      |
// | std::function     | 高     | 中   | ✗      | ✓      |
// | CRTP              | 低     | 高   | ✓      | ✗      |
// | Policy-Based      | 中     | 高   | ✓      | ✗      |
// | if constexpr      | 低     | 最高 | ✓      | ✗      |
// | Concepts          | 中     | 高   | ✓      | ✗      |
// | 类型擦除 (手动)   | 高     | 中   | ✗      | ✓      |

// 选择原则：
// 1. 不确定 → 用虚函数（最安全的默认）
// 2. 确定类型在编译时已知 → 用模板
// 3. 需要运行时切换 → 虚函数或 std::function
// 4. 性能关键 → 模板 / constexpr
// 5. API 稳定性 → 类型擦除隐藏模板
```

## 实际项目建议

```cpp
// 1. 默认使用 Rule of 0
//    - 用 unique_ptr/shared_ptr 管理资源
//    - 用标准容器管理数据
//    - 让编译器生成特殊成员函数

// 2. 优先值语义而非引用语义
//    - 传值 + std::move 优于传指针
//    - 用 optional 表达可空性

// 3. 资源管理 = RAII，无例外
//    - 永远不用裸 new/delete
//    - 自定义资源写 RAII 包装类

// 4. 编译时 > 运行时（但不要过度）
//    - 能用 constexpr 的用 constexpr
//    - 能用 Concepts 约束的用 Concepts
//    - 但别为了编译时多态把代码搞成天书

// 5. 模板仅在库和通用工具中使用
//    - 业务代码不需要 CRTP 或 Policy-Based Design
//    - 通用工具用模板，具体业务用虚函数
```

> [!tip] 关键要点
> **没有银弹**。选择模式时问三个问题：(1) 类型在编译时确定吗？(2) 需要运行时切换行为吗？(3) 性能瓶颈在哪里？大多数应用代码应该追求**清晰度而非极致性能**——虚函数的开销在绝大多数场景中可以忽略。只在 hot path 中才值得用编译时多态换取性能。

> [!info] C++20 对模式的影响
> **Concepts** 替代了大部分 SFINAE 和 CRTP 的接口检查用途。**Ranges** 替代了手写迭代器循环。**std::variant + std::visit** 替代了 Visitor 模式。**consteval/constexpr** 让更多计算在编译时完成。现代 C++ 让经典模式更简洁，但设计思想本身永不过时。

## 相关链接

- [[设计模式概述]] — GoF 经典设计模式全景
- [[cpp-raii-惯用法]] — C++ 最核心的惯用法
- [[cpp-crtp-奇异递归模板模式]] — 编译时多态的代表
- [[cpp-策略设计]] — 编译时策略组合
- [[cpp-类型擦除]] — 运行时多态的现代实现
- [[cpp-sfinae-与编译期多态]] — 编译期约束技术
