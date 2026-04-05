---
title: "Linux seccomp 系统调用过滤"
tags: [linux, seccomp, security, sandbox, syscall]
aliases: [seccomp, 系统调用过滤, BPF filter, 沙箱]
created: 2026-04-05
updated: 2026-04-05
---

# Linux seccomp 系统调用过滤

seccomp（Secure Computing）限制进程可用的系统调用，减少内核攻击面。

## 三种模式

| 模式 | 严格程度 | 用途 |
|------|----------|------|
| SECCOMP_MODE_STRICT | 只允许 read/write/exit/sigreturn | 极端沙箱 |
| SECCOMP_MODE_FILTER | BPF 过滤器自定义规则 | 容器/Docker |
| SECCOMP_MODE_DISABLED | 不过滤 | 默认 |

## seccomp-bpf 过滤

```c
#include <linux/seccomp.h>
#include <linux/filter.h>
#include <sys/prctl.h>

// 只允许必要的系统调用
struct sock_filter filter[] = {
    BPF_STMT(BPF_LD | BPF_W | BPF_ABS, offsetof(struct seccomp_data, nr)),
    BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, __NR_read, 0, 1),
    BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ALLOW),
    BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, __NR_write, 0, 1),
    BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ALLOW),
    BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_KILL),  // 其他全部拒绝
};

struct sock_fprog prog = { .len = sizeof(filter)/sizeof(filter[0]), .filter = filter };
prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0);
seccomp(SECCOMP_SET_MODE_FILTER, 0, &prog);
```

## Docker seccomp

```bash
# 查看默认 profile
docker inspect --format='{{.HostConfig.SecurityOpt}}' container

# 自定义 profile
docker run --security-opt seccomp=custom-profile.json nginx

# 无 seccomp（不推荐）
docker run --security-opt seccomp=unconfined nginx
```

## 工具

```bash
# strace 查看系统调用
strace -c ./app                # 统计调用次数
strace -e trace=network ./app  # 只看网络调用

# scmp_sys_resolver（系统调用号查询）
scmp_sys_resolver execve       # → 59
```

## 关联
- [[linux-BPF-与-eBPF]] — seccomp 使用 BPF 过滤器
- [[linux-Docker-基础]] — Docker 默认使用 seccomp

## 关键结论

> Docker 默认 seccomp profile 禁用了约 44 个危险系统调用（如 keyctl、add_key、mount）。自定义 profile 可以进一步收紧，但需要仔细测试应用依赖的系统调用。
