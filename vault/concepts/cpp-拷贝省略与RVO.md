---
title: 拷贝省略与 RVO
tags: [cpp, copy-elision, RVO, NRVO, mandatory-elision, C++17]
aliases: [拷贝省略, RVO, NRVO, 返回值优化, 强制省略, copy elision]
created: 2026-04-04
updated: 2026-04-04
---

# 拷贝省略与 RVO

拷贝省略让编译器跳过不必要的拷贝/移动构造——C++17 将部分省略变为强制，让返回大对象真正零开销。

## RVO 与 NRVO

```cpp
Widget create_widget() {
    Widget w;            // 在调用者的栈帧上构造（省略了拷贝）
    w.configure();
    return w;            // 不调用移动/拷贝构造
}

auto w = create_widget();  // w 就是函数内部的 w

// RVO (Return Value Optimization)：返回临时对象时省略拷贝
Widget create() {
    return Widget{1, 2, 3};  // 直接在调用者位置构造
}

// NRVO (Named RVO)：返回命名对象时省略拷贝
Widget create_named() {
    Widget result;            // 编译器可能做 NRVO
    result.init();
    return result;            // 可能省略拷贝/移动
}
```

## C++17 强制省略

```cpp
// C++17：以下场景必须省略（即使移动构造函数被删除也行）
struct NoMove {
    NoMove() = default;
    NoMove(const NoMove&) = delete;
    NoMove(NoMove&&) = delete;
};

NoMove create() {
    return NoMove{};  // C++17 前：编译错误（需要移动构造）
                      // C++17：OK，强制省略
}

NoMove obj = NoMove{};  // 同上：强制省略
```

## ⚠️ 不要依赖 NRVO

```cpp
// NRVO 不是强制的——不同编译器/条件可能不触发
Widget create(bool flag) {
    Widget w1, w2;
    return flag ? w1 : w2;  // NRVO 不适用于此（编译器无法确定返回哪个）
    // 会调用移动构造
}

// 安全做法：即使 NRVO 不触发，移动语义保证了合理性能
```

## 关键要点

> C++17 使"prvalue 初始化对象"成为强制省略——即使删除了拷贝和移动构造也能编译。NRVO（命名对象）仍是可选的优化。

> 不要为了 RVO 而扭曲代码结构——移动语义已经让"返回大对象"的开销降到很低。

## 相关模式 / 关联

- [[cpp-右值引用与移动语义]] — 拷贝省略失效时的后备
- [[cpp-类与对象]] — 构造函数与拷贝控制
