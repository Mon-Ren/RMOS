---
title: "Linux AppArmor 实战配置"
tags: [linux, apparmor, security, profile, sandbox]
aliases: [AppArmor实战, aa-genprof, profile, 强制访问控制]
created: 2026-04-05
updated: 2026-04-05
---

# Linux AppArmor 实战配置

AppArmor 基于路径的强制访问控制，比 SELinux 更易上手，适合中小规模部署。

## Profile 模式

| 模式 | 说明 |
|------|------|
| enforce | 强制执行，违规拒绝 |
| complain | 只记录不拒绝（学习模式） |
| disable | 禁用 |

## 从零创建 Profile

```bash
# 1. 切换到 complain 模式（学习）
aa-complain /usr/bin/myapp

# 2. 正常使用应用，触发各种操作
myapp --do-something

# 3. 从日志生成 profile
aa-genprof /usr/bin/myapp
# 交互式：对每个事件选择 allow/deny

# 4. 切换到 enforce
aa-enforce /usr/bin/myapp
```

## Profile 语法

```
#include <tunables/global>

/usr/bin/myapp {
  #include <abstractions/base>
  #include <abstractions/nameservice>

  /etc/myapp/** r,                    # 只读配置
  /var/log/myapp/** w,               # 可写日志
  /var/lib/myapp/ rw,                # 读写数据目录
  /var/lib/myapp/** rwk,             # 读写+锁
  /tmp/myapp-* rw,                   # 临时文件
  
  capability net_bind_service,       # 绑定低端口
  network tcp,                       # TCP 网络
  
  deny /etc/shadow r,                # 显式拒绝
}
```

## 管理

```bash
# 状态
aa-status
aa-status | grep enforce

# 重新加载
systemctl reload apparmor

# 禁用单个 profile
ln -s /etc/apparmor.d/usr.bin.myapp /etc/apparmor.d/disable/
apparmor_parser -R /etc/apparmor.d/usr.bin.myapp
```

## 关联
- [[linux-SELinux-与-AppArmor]] — SELinux vs AppArmor 对比
- [[linux-seccomp-系统调用过滤]] — 配合 seccomp 加固

## 关键结论

> AppArmor 的优势是基于路径（不需要给文件打标签），profile 就是普通文本文件，可以用版本控制管理。compose 模式可以逐步收紧权限：先 complain 收集事件，再 enforce 拒绝未授权访问。
