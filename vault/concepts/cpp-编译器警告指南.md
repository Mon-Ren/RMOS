---
title: C++ 编译器警告指南
tags: [cpp, warning, compiler-warning, -Wall, -Wextra, diagnostics]
aliases: [编译器警告, -Wall, -Wextra, 警告指南, 诊断信息]
created: 2026-04-04
updated: 2026-04-04
---

# C++ 编译器警告指南

编译器警告是免费的代码审查——开启所有合理警告并当作错误处理。

## 推荐的警告选项

```bash
# GCC/Clang 基础警告
-Wall -Wextra -Wpedantic

# 更严格的警告
-Wall -Wextra -Wpedantic -Werror        # 所有警告当错误
-Wshadow                                 # 变量遮蔽
-Wconversion                             # 隐式类型转换
-Wsign-conversion                        # 有符号/无符号转换
-Wnon-virtual-dtor                       # 非虚析构
-Wold-style-cast                         # C 风格转换
-Wcast-align                             # 对齐变更的转换
-Woverloaded-virtual                     # 隐藏基类虚函数
-Wnull-dereference                       # 空指针解引用

# MSVC
/W4 /WX                                  # 最高级别警告 + 当错误
/permissive-                             # 严格模式
```

## 常见警告及修复

```cpp
// -Wshadow：变量遮蔽
int x = 10;
void foo() {
    int x = 20;  // ⚠️ 遮蔽外层 x
}
// 修复：用不同名字

// -Wsign-conversion：有符号/无符号混合
int i = -1;
unsigned u = 1;
if (i < u) { }  // ⚠️ i 被转为巨大的 unsigned
// 修复：显式转换或统一类型

// -Wconversion：隐式窄化
double d = 3.14;
int n = d;  // ⚠️ 精度丢失
// 修复：static_cast<int>(d)

// -Wnon-virtual-dtor：基类无虚析构
class Base {
    virtual void foo();
    // ⚠️ 没有 virtual ~Base()
};
// 修复：加 virtual ~Base() = default;
```

## CMake 集成

```cmake
# 全局开启警告
add_compile_options(-Wall -Wextra -Wpedantic)

# 特定 target
target_compile_options(myapp PRIVATE
    -Wall -Wextra -Wpedantic -Werror
    -Wshadow -Wconversion
)

# MSVC
if(MSVC)
    target_compile_options(myapp PRIVATE /W4 /WX)
endif()
```

## 关键要点

> `-Wall -Wextra -Wpedantic -Werror` 是 C++ 项目的最低要求。在 CI 中强制执行——警告不处理就会变成 bug。

> `-Wshadow` 和 `-Wconversion` 特别有价值——它们捕获了大量隐蔽的逻辑错误。

## 相关模式 / 关联

- [[cpp-调试技术与断言]] — 运行时检查
- [[cpp-clang-tidy与静态分析]] — 更高级的静态分析
