---
title: 异常处理的零开销模型
tags: [cpp, exception, zero-cost, table-based, unwinding, landing-pad]
aliases: [零开销异常, table-based exceptions, 栈展开机制, landing pad]
created: 2026-04-05
updated: 2026-04-05
---

# 异常处理的零开销模型

**一句话概述：** C++ 异常的"零开销"模型意思是：正常执行路径上没有任何开销（不检查错误码、不插入额外指令），所有开销集中到异常抛出时——通过查表定位 catch、逐帧析构局部变量。代价是异常抛出极其慢（~微秒级），但正常路径极其快。

## 两种异常实现模型

```
模型 A：Code-based（早期 C++，MSVC /EHs 的旧模式）
──────────────────────────────────────────────
每个函数调用后插入检查代码：
  call foo
  test eax, eax    ← 检查是否抛异常
  jnz handle_error ← 跳转到处理代码

  正常路径开销：每次函数返回都多一次检查（~2-3 CPU 周期）
  异常路径开销：快（直接跳转）
  → 已淘汰，因为正常路径开销太大

模型 B：Table-based（现代实现，GCC/Clang/MSVC 默认）
──────────────────────────────────────────────
编译时生成异常处理表：
  .section .gcc_except_table   ← 异常表（只读段）
  .Lcatch_range:
    .long .Ltry_begin - .      ← try 块起始 PC
    .long .Ltry_end - .        ← try 块结束 PC
    .long .Llanding_pad - .    ← landing pad（catch 处理代码）
    .long 1                    ← catch 的类型索引

  正常路径开销：零（表在只读段，不影响代码执行）
  异常路径开销：高（查表 + 栈展开 + 逐帧析构）
  → 现代编译器的默认模式
```

## 异常抛出的完整流程

```
throw std::runtime_error("oops");
│
├─ ① 在堆上分配异常对象（__cxa_allocate_exception）
│  └─ 异常对象包含：用户数据 + typeinfo + cleanup 函数
│
├─ ② 查找 catch 处理器（__cxa_throw → _Unwind_RaiseException）
│  │
│  ├─ 遍历调用栈，对每一帧：
│  │   1. 根据当前 PC 在 .gcc_except_table 中查找
│  │   2. PC 是否在某个 try 块的范围内？
│  │      ├─ 是 → 检查 catch 类型是否匹配
│  │      │      ├─ 匹配 → 找到 landing pad，准备跳转
│  │      │      └─ 不匹配 → 继续向上查找
│  │      └─ 否 → 这一帧没有 try，进入栈展开
│  │
│  └─ 如果找到匹配的 catch：
│      ③ 栈展开（__cxa_begin_catch）
│         从 throw 点到 catch 点，逐帧：
│         - 调用局部变量的析构函数
│         - 如果是 catch-all(...)，也捕获
│         - 恢复栈指针到 catch 所在帧
│
│      ④ 跳转到 landing pad（catch 块的代码）
│         开始执行 catch { ... } 中的代码
│
└─ 如果找不到任何匹配的 catch：
   ⑤ 调用 std::terminate() → 默认调用 std::abort()
```

## 编译器生成的代码

```cpp
// 源代码
int example() {
    Resource r;           // RAII 对象
    if (something_wrong)
        throw std::runtime_error("error");
    return r.value();
}

// 编译器生成的伪代码（概念性）：
int example() {
    Resource r;
    r.constructor();      // 构造

    if (something_wrong) {
        // throw 之前不需要任何检查——直接执行
        // 异常表会记录 r 的析构函数
        void* ex = __cxa_allocate_exception(sizeof(std::runtime_error));
        new (ex) std::runtime_error("error");
        __cxa_throw(ex, &typeid(std::runtime_error), destructor<runtime_error>);
        // __cxa_throw 不返回（要么跳到 catch，要么 terminate）
    }

    int result = r.value();
    r.destructor();       // 正常析构
    return result;

    // 异常处理路径（Landing Pad）：
    // 只有异常抛出时才执行的代码
__landing_pad:
    r.destructor();       // 栈展开：析构 r
    __cxa_resume();       // 继续向上查找 catch
}
```

## 异常慢在哪里

```
throw 的成本分解（典型值，x86-64）：
┌──────────────────────────┬────────────┐
│ 操作                      │ 耗时       │
├──────────────────────────┼────────────┤
│ 分配异常对象              │ ~200 ns    │  ← malloc
│ 构造异常对象              │ ~100 ns    │  ← string copy
│ 调用 _Unwind_RaiseException │ ~50 ns  │
│ 查表（每个栈帧）          │ ~100 ns/帧 │  ← 二分查找
│ 栈展开（析构局部变量）    │ ~50 ns/帧  │
│ 跳转到 landing pad       │ ~20 ns     │
├──────────────────────────┼────────────┤
│ 总计（5 层调用栈）        │ ~1-5 μs    │  ← 微秒级！
└──────────────────────────┴────────────┘

对比：正常 return 一个值 = ~1 ns
→ 异常抛出比正常返回慢 1000-5000 倍
```

## 实践建议

```cpp
// ❌ 热循环中用异常做控制流
for (int i = 0; i < 1000000; ++i) {
    try {
        process(data[i]);
    } catch (const Error& e) {
        // 每 1000 次抛一次异常 → 性能灾难
    }
}

// ✅ 异常只用于真正异常的、不可恢复的情况
try {
    load_config("config.json");
} catch (const FileError& e) {
    // 配置文件不存在 → 这是"异常"情况，不是正常控制流
    use_defaults();
}

// ✅ 预期可能失败的操作用 expected/optional
std::expected<User, Error> find_user(int id);
auto user = find_user(42);
if (!user) { /* 处理未找到 */ }
```

## -fno-exceptions 的影响

禁用异常后：
- `throw` 变成 `std::terminate()` 调用（直接终止）
- 标准库的所有 `try`/`catch` 消失
- 生成的代码更小（异常表没了），但你失去了错误传播的能力
- 很多库（包括标准库）在禁用异常时行为不同

## 关键要点

> "零开销"指的是正常执行路径上没有开销，不是"异常抛出免费"。实际上异常抛出非常昂贵——这是为了正常路径的性能做出的权衡。

> 异常表存储在只读段，不占用运行时内存。但会使二进制文件变大（每个 try 块都有对应的表条目）。

> 在嵌入式和实时系统中通常禁用异常，因为异常抛出的时间不可预测（查表时间取决于栈深度，栈展开取决于有多少局部对象需要析构）。

## 相关模式 / 关联

- [[cpp-异常处理]] — try-catch 基础语法
- [[cpp-异常安全深入]] — 异常安全保证
- [[cpp-异常vs错误码]] — 错误处理策略选择
- [[cpp-expected]] — C++23 值或错误
- [[cpp-异常处理性能开销]] — 性能测量与分析
