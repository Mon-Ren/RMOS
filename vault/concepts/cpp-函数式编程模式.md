---
title: 函数式编程模式
tags: [cpp, idiom, functional, lambda, ranges]
aliases: [Functional C++, 函数式 C++, currying, partial application, std::bind, ranges]
created: 2026-04-04
updated: 2026-04-04
---

# Currying 与函数式 C++

**一句话概述：** 借助 lambda、`std::bind`、`std::function` 和 C++20 ranges，在 C++ 中实践函数式编程——部分应用、高阶函数、纯函数和不可变数据处理流水线。

## 意图与场景

C++ 从 C++11 起逐步增强函数式编程能力：

- **Lambda 表达式**：匿名函数，捕获上下文
- **高阶函数**：函数作为参数或返回值
- **部分应用 / Currying**：固定部分参数，生成新函数
- **Ranges（C++20）**：声明式数据处理流水线

**适用场景：**
- 事件回调系统
- 数据处理管道（ETL、转换、过滤）
- 策略/算法参数化
- 并行计算（纯函数天然线程安全）

## C++ 实现代码

### Lambda 与 std::function

```cpp
#include <functional>
#include <vector>
#include <algorithm>
#include <iostream>
#include <numeric>

void lambda_basics() {
    // Lambda 捕获
    int factor = 2;
    auto multiply = [factor](int x) { return x * factor; };      // 值捕获
    auto add      = [&factor](int x) { return x + factor; };     // 引用捕获
    auto generic  = [](auto x, auto y) { return x + y; };        // 泛型 lambda
    auto mutable_ = [count = 0]() mutable { return ++count; };   // mutable lambda
    
    // std::function：类型擦除的可调用对象
    std::function<int(int, int)> op = [](int a, int b) { return a + b; };
    op = std::multiplies<int>{};  // 切换为乘法
    std::cout << op(3, 4) << "\n";  // 12
}
```

### Partial Application 与 Currying

```cpp
#include <functional>
#include <iostream>

// 部分应用：固定某些参数
auto create_multiplier(int factor) {
    return [factor](int x) { return x * factor; };
}

// 更通用的部分应用
template <typename F, typename... BoundArgs>
auto partial(F&& func, BoundArgs&&... bound) {
    return [func = std::forward<F>(func), 
            ...bound = std::forward<BoundArgs>(bound)](auto&&... rest) {
        return func(bound..., std::forward<decltype(rest)>(rest)...);
    };
}

// 使用
void demo_partial() {
    auto double_of = create_multiplier(2);
    auto triple_of = create_multiplier(3);
    
    std::cout << double_of(21) << "\n";  // 42
    std::cout << triple_of(14) << "\n";  // 42
    
    // partial 示例
    auto add = [](int a, int b, int c) { return a + b + c; };
    auto add_5_10 = partial(add, 5, 10);
    std::cout << add_5_10(20) << "\n";  // 35
}

// Currying：将 f(a,b,c) 转为 f(a)(b)(c)
auto curry_add = [](int a) {
    return [a](int b) {
        return [a, b](int c) {
            return a + b + c;
        };
    };
};
// curry_add(1)(2)(3) == 6
```

### C++20 Ranges：声明式数据处理

```cpp
#include <ranges>
#include <vector>
#include <iostream>
#include <algorithm>
#include <string>

void ranges_demo() {
    std::vector<int> numbers = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    
    // 传统方式：多次遍历，产生中间容器
    // std::vector<int> filtered;
    // std::copy_if(numbers.begin(), numbers.end(), 
    //              std::back_inserter(filtered), [](int n) { return n % 2 == 0; });
    // std::vector<int> squared;
    // std::transform(filtered.begin(), filtered.end(),
    //                std::back_inserter(squared), [](int n) { return n * n; });
    
    // Ranges 方式：惰性求值，单次遍历，无中间容器
    auto result = numbers
        | std::views::filter([](int n) { return n % 2 == 0; })   // 过滤偶数
        | std::views::transform([](int n) { return n * n; })     // 求平方
        | std::views::take(3);                                    // 取前 3 个
    
    for (int n : result) {
        std::cout << n << " ";  // 4 16 36
    }
    
    // 范围算法（C++20）
    std::ranges::sort(numbers, std::greater<>{});  // 降序
    std::ranges::for_each(numbers, [](int n) { std::cout << n << " "; });
}
```

### 纯函数与不可变性

```cpp
#include <string>
#include <vector>
#include <algorithm>

// 纯函数：无副作用，相同输入 → 相同输出
auto pure_transform(const std::vector<int>& input, 
                    std::function<int(int)> func) -> std::vector<int> {
    std::vector<int> result;
    result.reserve(input.size());
    for (const auto& x : input) {
        result.push_back(func(x));
    }
    return result;
}

// 不可变数据流
struct Config {
    const std::string name;
    const int timeout;
    const bool verbose;
    
    // 返回新对象，而非修改原对象
    Config with_timeout(int t) const {
        return {name, t, verbose};
    }
    Config with_verbose(bool v) const {
        return {name, timeout, v};
    }
};

// 使用
void immutable_demo() {
    Config base{"default", 30, false};
    auto config = base.with_timeout(60).with_verbose(true);
    // base 保持不变
}
```

### 函数组合

```cpp
#include <utility>
#include <type_traits>

// 函数组合：compose(f, g)(x) == f(g(x))
template <typename F, typename G>
auto compose(F f, G g) {
    return [f = std::move(f), g = std::move(g)](auto&&... args) {
        return f(g(std::forward<decltype(args)>(args)...));
    };
}

// 管道：pipe(f, g, h)(x) == h(g(f(x)))
template <typename F, typename... Fs>
auto pipe(F first, Fs... rest) {
    if constexpr (sizeof...(rest) == 0) {
        return first;
    } else {
        return compose(pipe(rest...), first);
    }
}

void compose_demo() {
    auto add_one   = [](int x) { return x + 1; };
    auto double_it = [](int x) { return x * 2; };
    auto to_string = [](int x) { return std::to_string(x); };
    
    auto transform = pipe(add_one, double_it, to_string);
    std::cout << transform(5) << "\n";  // (5+1)*2 = 12 → "12"
}
```

## 优缺点

| 优点 | 缺点 |
|------|------|
| 代码更简洁、声明式 | lambda 捕获易引入悬挂引用 |
| 纯函数天然线程安全 | std::function 有类型擦除开销 |
| Ranges 惰性求值高效 | 调试时栈追踪不直观 |
| 函数组合提高复用性 | C++ ranges 学习曲线较陡 |

> [!tip] 关键要点
> C++ 不是函数式语言，但**函数式风格在 C++ 中非常实用**。优先使用 `std::views` 的惰性范围适配器代替创建中间容器。lambda 捕获时优先使用 `[=]` 或显式捕获，避免 `[&]` 捕获悬挂风险。C++20 ranges 让 C++ 的数据处理接近 Python/Scala 的表达力，同时保持 C++ 的性能。

## 相关链接

- [[策略模式]] — 函数对象作为策略注入
- [[Command 模式]] — std::function 实现命令队列
- [[cpp-类型擦除]] — std::function 的实现原理
- [[cpp-标签分发]] — ranges 内部使用 tag dispatch
