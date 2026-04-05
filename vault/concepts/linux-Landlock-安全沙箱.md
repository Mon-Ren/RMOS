---
title: "Linux Landlock 安全沙箱"
tags: [linux, landlock, security, sandbox, lsm]
aliases: [Landlock, 沙箱, 文件访问控制, 应用沙箱]
created: 2026-04-05
updated: 2026-04-05
---

# Linux Landlock 安全沙箱

Landlock 是 Linux 5.13+ 引入的非特权 LSM 沙箱框架，应用可以自主限制自己的文件系统访问。

## 核心特点

- **非特权**：不需要 root，普通进程即可使用
- **可组合**：进程只能收紧限制，不能放松
- **文件系统焦点**：主要限制文件访问
- **继承**：子进程自动继承沙箱规则

## 系统调用

```c
// 创建规则集
int ruleset_fd = landlock_create_ruleset(&ruleset_attr, sizeof(ruleset_attr), 0);

// 添加规则（允许访问 /usr）
struct landlock_path_beneath_attr path_attr = {
    .allowed_access = LANDLOCK_ACCESS_FS_READ_DIR | LANDLOCK_ACCESS_FS_READ_FILE,
    .parent_fd = open("/usr", O_PATH | O_CLOEXEC),
};
landlock_add_rule(ruleset_fd, LANDLOCK_RULE_PATH_BENEATH, &path_attr, 0);

// 启用沙箱
prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0);
landlock_restrict_self(ruleset_fd, 0);
// 此后进程只能访问 /usr，其他目录被拒绝
```

## 使用场景

- **编译器**：只允许读源码、写输出目录
- **文档处理器**：只允许读文档和字体
- **Web 应用**：只允许读静态文件
- **不受信任代码**：限制文件访问范围

## 与 seccomp/AppArmor 的对比

| | Landlock | seccomp | AppArmor |
|---|----------|---------|----------|
| 非特权 | ✅ | ✅ | ❌ |
| 限制维度 | 文件系统 | 系统调用 | 文件+网络+权限 |
| 配置方式 | 进程自限制 | BPF 过滤器 | 系统级 profile |
| 复杂度 | 低 | 中 | 高 |

## 关联
- [[linux-seccomp-系统调用过滤]] — 系统调用过滤
- [[linux-AppArmor-实战配置]] — AppArmor 沙箱

## 关键结论

> Landlock 的创新是"非特权沙箱"：不需要 root 或管理员配置，应用自己限制自己。特别适合运行不受信任的第三方工具或插件。
