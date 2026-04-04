---
title: 迭代器失效规则汇总
tags: [cpp, stl, iterator-invalidation, dangling-iterator, container-modification]
aliases: [迭代器失效, iterator invalidation, 容器修改, 悬垂迭代器]
created: 2026-04-04
updated: 2026-04-04
---

# 迭代器失效规则汇总

修改容器后哪些迭代器还有效？这是 STL 最容易犯错的知识点。

## vector

```
操作              迭代器/指针/引用失效
──────────────────────────────────────
push_back         不扩容时：end() 之外不失效
                  扩容时：全部失效
insert            插入点及之后失效
erase             被删点及之后失效
clear             全部失效
reserve           如果触发重新分配：全部失效
resize            同 push_back/erase
```

## deque

```
操作              迭代器失效
──────────────────────────────────────
push_front/push_back  所有迭代器失效（但指针/引用可能不失效）
insert/erase          所有迭代器失效
```

## list / forward_list

```
操作              迭代器失效
──────────────────────────────────────
insert/splice     不失效（list 的核心优势）
erase             仅被删元素的迭代器失效
```

## map / set（红黑树）

```
操作              迭代器失效
──────────────────────────────────────
insert            不失效
erase             仅被删元素的迭代器失效
```

## unordered_map / unordered_set（哈希表）

```
操作              迭代器失效
──────────────────────────────────────
insert            不触发 rehash 时不失效
                  触发 rehash 时：全部失效
erase             仅被删元素的迭代器失效
```

## 安全的删除模式

```cpp
// vector：erase 返回下一个有效迭代器
for (auto it = v.begin(); it != v.end(); ) {
    if (should_remove(*it))
        it = v.erase(it);
    else
        ++it;
}

// map：C++17 前
for (auto it = m.begin(); it != m.end(); ) {
    if (should_remove(it))
        m.erase(it++);  // it++ 先递增再删除旧位置
    else
        ++it;
}

// map：C++17 erase 返回下一个迭代器
for (auto it = m.begin(); it != m.end(); ) {
    if (should_remove(it))
        it = m.erase(it);
    else
        ++it;
}
```

## 关键要点

> `vector`/`deque` 的修改使大量迭代器失效——修改后必须重新获取迭代器。`list`/`map` 的迭代器稳定性是选择它们的核心理由。

> 删除元素时永远用 `erase` 的返回值更新迭代器——自增后再删除是经典 bug。

## 相关模式 / 关联

- [[cpp-vector深入]] — vector 的迭代器失效
- [[cpp-map与set]] — 红黑树容器的迭代器稳定性
