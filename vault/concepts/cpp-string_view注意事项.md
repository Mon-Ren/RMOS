---
title: string_view 使用注意事项
tags: [cpp17, string_view, lifetime, dangling, non-owning, string]
aliases: [string_view注意, 生命周期, 悬垂string_view, string_view陷阱]
created: 2026-04-04
updated: 2026-04-04
---

# string_view 使用注意事项

`string_view` 是零拷贝的字符串引用——性能优秀但有生命周期陷阱，使用不当会悬垂。

## 安全用法

```cpp
// ✅ 函数参数：安全
void process(std::string_view sv) {
    // sv 不拥有数据，调用者保证数据存活
}

process("literal");            // 字面量存活于程序整个生命周期
process(existing_string);      // existing_string 存活于调用期间

// ✅ 函数返回字面量：安全
std::string_view get_name() {
    return "fixed_name";  // OK：字面量永久有效
}
```

## 危险用法

```cpp
// ❌ 返回局部 string 的 string_view
std::string_view bad_return() {
    std::string s = "oops";
    return s;  // s 销毁后 sv 悬垂！
}

// ❌ 返回临时 string 的 string_view
std::string_view bad2() {
    return get_string() + " suffix";  // 临时 string 销毁！
}

// ❌ 从 c_str() 获得的 string_view
std::string_view bad3() {
    const char* p = get_temp_string().c_str();
    return p;  // 临时 string 销毁，p 悬垂！
}

// ❌ string_view 存储在比源 string 更长的生命周期中
class Config {
    std::string_view name_;  // 危险：不拥有数据
public:
    Config(std::string_view n) : name_(n) {}  // 调用者的 string 必须存活
};
```

## 安全模式

```cpp
// ✅ 类成员用 string（拥有数据）
class Config {
    std::string name_;       // 拥有数据
public:
    Config(std::string_view n) : name_(n) {}  // 拷贝一份
    std::string_view name() const { return name_; }  // 返回 view
};

// ✅ 临时使用时立即消费
void safe(std::string_view sv) {
    size_t len = sv.size();    // 立即使用
    char c = sv[0];            // 立即使用
    // 不存储 sv 到成员/全局变量
}
```

## 关键要点

> `string_view` 是非拥有引用——指向的数据必须在 view 的整个生命周期内存活。用它做函数参数很安全，做返回值和成员变量要小心。

> 当不确定生命周期时，用 `std::string` 拥有数据，返回 `string_view` 供临时读取。

## 相关模式 / 关联

- [[cpp-string深入]] — string 与 string_view 的配合
- [[cpp-span]] — span 是 string_view 的泛化
