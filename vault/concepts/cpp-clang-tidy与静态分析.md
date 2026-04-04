---
title: clang-tidy 与静态分析
tags: [cpp, clang-tidy, static-analysis, cppcheck, lint, code-quality]
aliases: [clang-tidy, 静态分析, cppcheck, lint, 代码质量工具]
created: 2026-04-04
updated: 2026-04-04
---

# clang-tidy 与静态分析

`clang-tidy` 是 C++ 的 linter——自动检查代码风格、bug、性能问题和现代 C++ 用法。

## 基本用法

```bash
# 检查单个文件
clang-tidy main.cpp -- -std=c++20

# 检查整个项目（需要 compile_commands.json）
clang-tidy -p build/ main.cpp

# 自动修复
clang-tidy main.cpp --fix -- -std=c++20

# 使用配置文件
clang-tidy -config-file=.clang-tidy main.cpp
```

## .clang-tidy 配置

```yaml
Checks: >
  -*,
  bugprone-*,
  modernize-*,
  performance-*,
  readability-*,
  -modernize-use-trailing-return-type

CheckOptions:
  - key: modernize-use-nullptr.NullMacros
    value: 'NULL'
  - key: readability-identifier-naming.ClassCase
    value: CamelCase
  - key: readability-identifier-naming.FunctionCase
    value: CamelCase
```

## 常用检查项

```
bugprone-*           常见 bug
  bugprone-use-after-move
  bugprone-narrowing-conversions

modernize-*          现代 C++ 用法
  modernize-use-auto
  modernize-use-nullptr
  modernize-use-emplace
  modernize-loop-convert

performance-*        性能问题
  performance-unnecessary-value-param
  performance-move-const-arg

readability-*        可读性
  readability-braces-around-statements
  readability-identifier-naming

cppcoreguidelines-*  C++ Core Guidelines
  cppcoreguidelines-owning-memory
  cppcoreguidelines-no-malloc
```

## 集成到 CI

```yaml
# GitHub Actions 示例
- name: clang-tidy
  run: |
    clang-tidy -p build/ $(find . -name "*.cpp" -not -path "./build/*") \
      --warnings-as-errors='*'
```

## 关键要点

> clang-tidy 能自动修复很多问题——先 `--fix` 自动修，再人工审查剩余。

> 在 CI 中用 `--warnings-as-errors='*'` 将警告视为错误——强制代码质量。

## 相关模式 / 关联

- [[cpp-调试技术与断言]] — 运行时检查
- [[cpp-代码审查清单]] — 人工审查
