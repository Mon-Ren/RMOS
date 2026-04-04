---
title: std::any 与 std::variant 对比
tags: [cpp, any, variant, comparison, type-safety, dynamic-type]
aliases: [any vs variant, 类型安全对比, 动态类型vs静态类型]
created: 2026-04-04
updated: 2026-04-04
---

# std::any 与 std::variant 对比

两者都是"存储不同类型"的方案——选择取决于类型集合是否在编译期已知。

## 对比

```
                    any                    variant<Ts...>
类型集合            完全动态（任意类型）      编译期固定
类型检查            运行时（type_info）       编译期 + 运行时
访问方式            any_cast（可能抛异常）     get<> / visit（编译期安全）
内存布局            可能堆分配               栈上分配（最大类型 + 标签）
性能                较慢（类型擦除）          较快
值语义              支持                     支持
默认构造            空                       需要第一个类型可默认构造
适用场景            插件系统、配置未知类型    状态机、AST、JSON 值
```

## 何时选哪个

```cpp
// 选 variant：类型集合在编译期已知
using JsonValue = std::variant<
    std::nullptr_t, bool, double,
    std::string, std::vector<JsonValue>,
    std::map<std::string, JsonValue>
>;

// 选 any：完全不知道会有什么类型
std::map<std::string, std::any> config;
config["timeout"] = 30;
config["name"] = std::string("app");
config["debug"] = true;
// 任何类型都可以塞进去

// 选 optional：只有"有值/无值"两种状态
std::optional<int> find(int key);
```

## 关键要点

> 90% 的"多类型"场景用 `variant`——类型集合已知时它更安全、更快。`any` 适用于真正的"未知类型"场景（配置系统、插件接口）。

> `variant` 可以递归（variant 包含 variant），`any` 不行。

## 相关模式 / 关联

- [[cpp-any]] — any 专题
- [[cpp-variant]] — variant 专题
- [[cpp-optional]] — optional 专题
