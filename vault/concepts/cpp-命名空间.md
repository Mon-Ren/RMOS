---
title: 命名空间
tags: [cpp, fundamentals, namespace, using, scope]
aliases: [命名空间, namespace, using声明, using指令, 匿名命名空间]
created: 2026-04-04
updated: 2026-04-04
---

# 命名空间

命名空间是 C++ 防止名称冲突的机制——在大型项目和多库协作中不可或缺。

## 意图与场景

- 避免全局命名冲突
- 组织相关代码为逻辑分组
- 版本管理（如 `std::ranges` vs `std`）

## 基本用法

```cpp
namespace math {
    constexpr double pi = 3.14159265358979;

    double circle_area(double r) {
        return pi * r * r;
    }

    // 嵌套命名空间（C++17 简写）
    namespace geometry::detail {
        double distance(double x1, double y1, double x2, double y2);
    }
    // C++17 等价于：
    // namespace math { namespace geometry { namespace detail { } } }
}

// 使用
double a = math::circle_area(5.0);
using math::pi;  // using 声明：引入单个名称
double c = 2 * pi * r;

// using 指令（不推荐在头文件中使用）
using namespace math;  // 引入整个命名空间
double d = circle_area(3.0);
```

## 匿名命名空间

```cpp
// 匿名命名空间：内部链接，等价于 static
namespace {
    int helper_count = 0;  // 仅在此编译单元可见
    void internal_helper() { /* ... */ }
}

// 等价于：
static int helper_count = 0;
static void internal_helper() { }
// 但匿名命名空间可以包含类型定义
```

## 内联命名空间（C++11）

```cpp
namespace lib {
    inline namespace v2 {    // 默认版本
        void process() { /* v2 实现 */ }
    }
    namespace v1 {           // 旧版本，仍可访问
        void process() { /* v1 实现 */ }
    }
}

lib::process();      // 调用 v2::process
lib::v1::process();  // 显式调用 v1::process
// ABI 版本管理利器
```

## 最佳实践

```cpp
// 头文件中：
// ✅ 使用完全限定名
namespace mylib {
    void foo();  // 声明
}

// ✅ 使用 using 声明（限定范围内）
namespace mylib {
    using std::string;  // 可以
}

// ❌ 头文件中不要 using namespace std;

// 源文件中：
using namespace std;  // 源文件可以接受
using std::vector;    // using 声明更安全
```

## 关键要点

> 头文件中永远不要写 `using namespace`——它会污染所有包含该头文件的编译单元的命名空间。

> 匿名命名空间是现代 C++ 中替代 `static` 关键字做内部链接的首选方式。

## 相关模式 / 关联

- [[cpp-模板编程基础]] — 模板与 ADL（参数依赖查找）
