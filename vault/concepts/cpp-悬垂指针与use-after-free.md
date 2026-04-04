---
title: 悬垂指针与 Use-After-Free
tags: [cpp, dangling-pointer, use-after-free, UAF, lifetime, safety]
aliases: [悬垂指针, use-after-free, UAF, 生命周期, 悬垂引用, 安全]
created: 2026-04-04
updated: 2026-04-04
---

# 悬垂指针与 Use-After-Free

悬垂指针指向已释放的内存——访问它是 UB，是最常见也是最危险的 C++ bug 之一。

## 常见来源

```cpp
// 1. 返回局部变量的指针/引用
int* bad() {
    int x = 42;
    return &x;  // x 在函数返回后销毁
}

// 2. 容器扩容使迭代器/引用失效
std::vector<int> v = {1, 2, 3};
int& ref = v[0];
v.push_back(4);   // 可能触发扩容，ref 现在悬垂
// ref = 100;       // UB！

// 3. 删除元素后使用迭代器
std::vector<int> v = {1, 2, 3};
auto it = v.begin();
v.erase(it);      // it 悬垂
// *it;              // UB！

// 4. 对象所有权不明确
Widget* create() { return new Widget(); }
void use() {
    Widget* p = create();
    // ... 使用 ...
    delete p;
    // p 现在悬垂，p = dangling pointer
    p->method();  // UB!
}

// 5. 异步任务引用局部变量
std::future<int> bad_async() {
    int local = 42;
    return std::async([&]() { return local; });  // 悬垂引用！
}
```

## 防御手段

```cpp
// 1. 用智能指针管理生命周期
auto p = std::make_unique<Widget>();  // 离开作用域自动释放

// 2. 用 string_view/span 前确认底层数据存活
void safe_process(std::string_view sv);  // 调用者保证 string 存活

// 3. ASan 检测
// g++ -fsanitize=address -g main.cpp

// 4. 避免裸指针做所有权
// 裸指针 = "不拥有"（观察者语义）
// unique_ptr = "独占拥有"
// shared_ptr = "共享拥有"
```

## 关键要点

> ASan（AddressSanitizer）是检测悬垂指针和 use-after-free 的最强工具——开发阶段必须开启。

> 裸指针在现代 C++ 中表示"不拥有，仅观察"——所有权用智能指针管理。

## 相关模式 / 关联

- [[cpp-智能指针对比与最佳实践]] — 用智能指针避免悬垂指针
- [[cpp-调试技术与断言]] — ASan 的使用
