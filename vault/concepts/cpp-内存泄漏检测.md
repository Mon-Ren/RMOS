---
title: C++ 与内存泄漏检测
tags: [cpp, memory-leak, leak-detection, ASan, valgrind, heaptrack]
aliases: [内存泄漏, leak detection, ASan, valgrind, heaptrack, 泄漏检测]
created: 2026-04-04
updated: 2026-04-04
---

# C++ 与内存泄漏检测

内存泄漏是 C++ 的经典问题——现代工具能在开发阶段自动发现大部分泄漏。

## 常见泄漏来源

```cpp
// 1. 忘记 delete
void leak1() {
    int* p = new int(42);
    // 忘记 delete p;
}

// 2. 异常路径上的泄漏
void leak2() {
    int* p = new int(42);
    throw std::runtime_error("oops");  // p 泄漏！
    delete p;  // 永远不会执行
}

// 3. 容器中的指针
void leak3() {
    std::vector<Widget*> widgets;
    widgets.push_back(new Widget());
    widgets.push_back(new Widget());
    // widgets.clear();  // 泄漏！指针不被 delete
}

// 4. 循环引用（shared_ptr）
struct Node {
    std::shared_ptr<Node> next;
    std::shared_ptr<Node> prev;  // 应该用 weak_ptr
};
```

## 检测工具

```bash
# AddressSanitizer（ASan）：泄漏 + UAF + 越界
g++ -fsanitize=address -g main.cpp -o main
# 环境变量控制：
ASAN_OPTIONS=detect_leaks=1 ./main

# Valgrind（Linux）：全面的内存检查
valgrind --leak-check=full --show-leak-kinds=all ./main
# 输出：definitely lost, indirectly lost, possibly lost, still reachable

# heaptrack：快速的堆分析
heaptrack ./program
heaptrack_gui heaptrack.program.*.gz

# LeakSanitizer（独立版本，Linux）
g++ -fsanitize=leak -g main.cpp -o main
```

## 防御手段

```cpp
// 1. 用 RAII 代替裸 new/delete
auto p = std::make_unique<int>(42);  // 自动释放

// 2. 容器中的指针用智能指针
std::vector<std::unique_ptr<Widget>> widgets;
widgets.push_back(std::make_unique<Widget>());  // 自动释放

// 3. 循环引用用 weak_ptr
struct Node {
    std::shared_ptr<Node> next;
    std::weak_ptr<Node> prev;  // 打破循环
};

// 4. Rule of Zero：让编译器生成正确的析构函数
```

## 关键要点

> 开发阶段始终开启 ASan——它能检测泄漏、UAF、越界等大部分内存错误，性能代价很小。

> `valgrind` 更全面但更慢——适合做最终的内存检查。`heaptrack` 是介于两者之间的轻量工具。

## 相关模式 / 关联

- [[cpp-调试技术与断言]] — 调试工具
- [[cpp-智能指针对比与最佳实践]] — 用智能指针避免泄漏
