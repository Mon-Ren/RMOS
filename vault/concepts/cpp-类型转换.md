---
title: 类型转换
tags: [cpp, fundamentals, cast, type-conversion]
aliases: [类型转换, cast, static_cast, dynamic_cast, const_cast, reinterpret_cast]
created: 2026-04-04
updated: 2026-04-04
---

# C++ 类型转换

C++ 的四种命名转换是编译器可审查的安全阀，C 风格转型则是什么都能过的万能钥匙——前者是工具，后者是危险。

## 意图与场景

- 明确转换意图，让编译器帮助检查合法性
- 替代 C 风格 `(type)` 转换，提高代码可读性和安全性

## 四种命名转换

### static_cast

编译期检查，最常见的转换：

```cpp
// 基本类型转换
double d = 3.14;
int i = static_cast<int>(d);  // i = 3，截断

// 向上转型（安全）
class Base {};
class Derived : public Base {};
Derived derived;
Base* bp = static_cast<Base*>(&derived);  // OK

// 向下转型（不检查，不安全）
Base* bp2 = new Derived();
Derived* dp = static_cast<Derived*>(bp2);  // 编译OK，但如果 bp2 不指向 Derived 则未定义行为

// void* 转换
void* vp = &i;
int* ip = static_cast<int*>(vp);  // OK

// 枚举转换
enum Color { Red, Green, Blue };
int c = static_cast<int>(Red);  // 0
```

### dynamic_cast

运行时类型检查，需要多态类型（至少一个虚函数）：

```cpp
class Base { virtual ~Base() = default; };
class Derived : public Base { void special() {} };
class Other : public Base {};

Base* bp = new Derived();

// 向下转型：成功
Derived* dp = dynamic_cast<Derived*>(bp);  // OK，dp 非 null

// 向下转型：失败返回 nullptr
Base* bp2 = new Other();
Derived* dp2 = dynamic_cast<Derived*>(bp2);  // dp2 == nullptr

// 引用版本：失败抛出 std::bad_cast
try {
    Derived& dr = dynamic_cast<Derived&>(*bp2);
} catch (const std::bad_cast& e) {
    // 处理失败
}
```

### const_cast

移除或添加 const 属性：

```cpp
void legacy_api(char* s);  // C 库函数，不修改但没声明 const

void wrapper(const char* s) {
    // legacy_api(s);              // 编译错误
    legacy_api(const_cast<char*>(s));  // OK，保证 legacy_api 不修改
}

// 危险：原始对象不是 const 时才能用 const_cast 修改
const int x = 42;
int* p = const_cast<int*>(&x);
*p = 100;  // 未定义行为！x 本身是 const
```

### reinterpret_cast

底层位模式重新解释，最危险的转换：

```cpp
int x = 42;
// 将 int 的位模式当作指针（极端危险示例）
intptr_t addr = reinterpret_cast<intptr_t>(&x);

// 类型双关（type punning）——不推荐
float f = 3.14f;
uint32_t bits = reinterpret_cast<uint32_t&>(f);  // 未定义行为！
// 应该用 memcpy 或 std::bit_cast（C++20）
```

## C++20 std::bitcast

```cpp
#include <bit>

float f = 3.14f;
uint32_t bits = std::bit_cast<uint32_t>(f);  // 安全的位模式复制
// 编译期可求值，无 UB
```

## 关键要点

> 优先级：`static_cast` > `dynamic_cast` > 极少用 `const_cast` > 几乎不用 `reinterpret_cast`。永远避免 C 风格转型。

> `dynamic_cast` 是唯一运行时安全的向下转型，但有性能开销（RTTI）。设计良好的代码应尽量避免向下转型。

## 相关模式 / 关联

- [[cpp-多态与虚函数]] — dynamic_cast 依赖虚函数表
- [[cpp-基本数据类型]] — 隐式转换规则
