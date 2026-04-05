---
title: "Linux kpatch 热补丁"
tags: [linux, kpatch, livepatch, 热更新, 内核]
aliases: [kpatch, livepatch, 热补丁, 在线修复, 内核热更新]
created: 2026-04-05
updated: 2026-04-05
---

# Linux kpatch 热补丁

kpatch/livepatch 允许在不重启系统的情况下修补运行中的内核，适用于高可用性场景。

## 原理

```
原始函数: old_func() { ... }
         ↓ 编译补丁
新函数: patched_func() { ... }   ← 从补丁 .ko 加载

运行时：
1. ftrace 将 old_func 入口重定向到 patched_func
2. 等待所有 CPU 离开 old_func（grace period）
3. patched_func 生效
```

## kpatch 使用

```bash
# 安装
apt install kpatch              # 部分发行版
yum install kpatch-dnf          # RHEL

# 制作补丁
kpatch-build fix.patch -t vmlinux

# 加载补丁
kpatch load kpatch-fix.ko

# 查看
kpatch list
# Loaded patch modules:
# kpatch-fix [enabled]

# 卸载
kpatch unload kpatch-fix
```

## 内核 livepatch API

```c
// 补丁模块注册
static struct klp_func funcs[] = {
    { .old_name = "old_func", .new_func = new_func },
    { }
};
static struct klp_object objs[] = {
    { .funcs = funcs },
    { }
};
static struct klp_patch patch = {
    .mod = THIS_MODULE,
    .objs = objs,
};
// module_init → klp_register_patch → klp_enable_patch
```

## 限制

- 不能修改数据结构布局
- 不能修改函数签名
- 某些安全关键函数不可打补丁
- 补丁是临时方案，仍需计划重启

## 关联
- [[linux-内核编译与配置]] — 内核编译
- [[linux-kprobe-与追踪基础设施]] — ftrace 基础

## 关键结论

> kpatch/livepatch 适合修复安全漏洞的紧急场景，避免立即重启。但它是临时措施，数据结构变更等复杂修复仍需完整内核升级。RHEL/SUSE/Ubuntu 都提供商业热补丁服务。
