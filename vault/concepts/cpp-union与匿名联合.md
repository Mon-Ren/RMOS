---
title: union 与匿名联合
tags: [cpp, union, anonymous-union, variant, type-punning]
aliases: [union, 联合体, 匿名联合, tagged union, type punning]
created: 2026-04-04
updated: 2026-04-04
---

# union 与匿名联合

C++ 的 union 在同一内存位置存储不同类型的值——类型不安全，现代代码应优先用 `std::variant`。

## 基本用法

```cpp
union Value {
    int    i;
    float  f;
    char   str[20];
};

Value v;
v.i = 42;           // 写入 int
std::cout << v.i;    // 读取 int：42
v.f = 3.14f;         // 写入 float（覆盖了 i）
std::cout << v.f;    // 读取 float：3.14
// std::cout << v.i;  // 未定义行为！f 覆盖了 i 的内存

// union 的大小 = 最大成员的大小（考虑对齐）
sizeof(Value);  // 至少 20（str 的大小）
```

## 匿名联合

```cpp
struct Variant {
    enum Type { Int, Float, String } type;
    union {
        int    i;
        float  f;
        char   str[20];
    };  // 匿名联合：直接访问成员

    void set_int(int val)   { type = Int;    i = val; }
    void set_float(float v) { type = Float;  f = v; }
};

Variant var;
var.set_int(42);
if (var.type == Variant::Int) {
    std::cout << var.i;  // OK，直接访问
}
```

## C++11 改进

```cpp
// union 可以有成员函数
union Value {
    int i;
    float f;

    Value() : i(0) {}               // 可以有构造函数
    ~Value() {}                     // 必须有析构函数（如果有非平凡成员）
};

// 带有非平凡类型的 union
union Data {
    std::string s;   // 非平凡类型
    std::vector<int> v;
    Data() {}        // 必须手动管理
    ~Data() {}       // 必须手动析构
};
// ⚠️ 极易出错 → 用 std::variant 替代
```

## 关键要点

> C 风格的 union 不追踪当前存储的类型——程序员必须自己维护，出错就是 UB。`std::variant` 用类型标签自动追踪，是现代替代。

> 匿名联合在 struct 内部使用时节省内存（互斥字段共享空间），但仍需手动管理类型标签。

## 相关模式 / 关联

- [[cpp-variant]] — 类型安全的 union 替代
- [[cpp-RTTI与typeid]] — 运行时类型判断
