---
title: C++ 智能指针与容器
tags: [cpp, smart-pointer, vector, unique-ptr, container, ownership]
aliases: [智能指针容器, vector of unique_ptr, 所有权管理容器]
created: 2026-04-04
updated: 2026-04-04
---

# 智能指针与容器

在容器中存储智能指针管理动态对象——`vector<unique_ptr<T>>` 是最常见的模式。

## vector of unique_ptr

```cpp
// 创建
std::vector<std::unique_ptr<Widget>> widgets;
widgets.push_back(std::make_unique<Widget>(1));
widgets.push_back(std::make_unique<Widget>(2));

// 移动到容器
auto ptr = std::make_unique<Widget>(3);
widgets.push_back(std::move(ptr));  // ptr 变为 null

// 删除
widgets.erase(widgets.begin());  // 自动 delete 第一个元素

// 查找后删除
auto it = std::find_if(widgets.begin(), widgets.end(),
    [](const auto& w) { return w->id() == 42; });
if (it != widgets.end()) widgets.erase(it);

// ⚠️ 不能用 initializer_list 初始化
// std::vector<std::unique_ptr<int>> v = {
//     std::make_unique<int>(1),  // 编译错误！initializer_list 要求拷贝
// };
```

## 多态容器

```cpp
std::vector<std::unique_ptr<Shape>> shapes;
shapes.push_back(std::make_unique<Circle>(5.0));
shapes.push_back(std::make_unique<Rectangle>(3.0, 4.0));

// 多态调用
for (const auto& shape : shapes) {
    std::cout << shape->area() << "\n";
}
```

## map 中的智能指针

```cpp
std::map<int, std::unique_ptr<Widget>> registry;

// 插入
registry[1] = std::make_unique<Widget>();

// 移动插入
auto w = std::make_unique<Widget>();
registry.insert({2, std::move(w)});

// 查找并使用
if (auto it = registry.find(1); it != registry.end()) {
    it->second->do_work();
}
```

## 关键要点

> `vector<unique_ptr<T>>` 是多态集合的标准模式——所有权明确（容器拥有所有元素），删除时自动释放。

> `initializer_list` 要求元素可拷贝——move-only 类型不能用初始化列表初始化容器，用 `push_back`/`emplace_back` 替代。

## 相关模式 / 关联

- [[cpp-智能指针对比与最佳实践]] — 智能指针选择
- [[cpp-move-only类型]] — unique_ptr 是 move-only
