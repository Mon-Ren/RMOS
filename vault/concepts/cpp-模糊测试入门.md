---
title: 模糊测试入门
tags: [cpp, fuzzing, libfuzzer, afl, security, testing]
aliases: [Fuzz 测试, libFuzzer, 覆盖率引导测试]
created: 2026-04-05
updated: 2026-04-05
---

# 模糊测试入门

**一句话概述：** 模糊测试（Fuzzing）通过随机/变异输入自动发现边界条件 bug。libFuzzer 基于覆盖率引导——优先探索未覆盖的代码路径。一行命令就能对解析器、编解码器、协议处理进行百万次变异测试。

```cpp
// fuzz target：接收任意字节输入
extern "C" int LLVMFuzzerTestOneInput(const uint8_t* data, size_t size) {
    std::string input(data, data + size);
    // 测试你的解析函数
    auto result = my_parser(input);
    return 0;  // 非零返回码保留
}

// 编译和运行
// clang++ -fsanitize=fuzzer,address -g parser.cpp -o fuzzer
// ./fuzzer corpus/  # corpus/ 是种子输入目录
// 发现的最小输入保存在 crash-<hash> 文件中
```

## 关键要点

> 模糊测试对解析器和编解码器特别有效——这些代码有大量分支取决于输入数据。覆盖率引导的 fuzzer 能在几小时内发现人类很难想到的边界条件。

## 相关模式 / 关联

- [[cpp-ASan-UBSan实战]] — Sanitizer 配合
- [[cpp-测试基础]] — 测试方法
- [[cpp-常见陷阱与反模式]] — 常见 bug
