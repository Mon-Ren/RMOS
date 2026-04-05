---
title: "Linux audit 审计系统"
tags: [linux, audit, security, compliance, auditd]
aliases: [audit, auditd, 审计, 安全审计, auditctl]
created: 2026-04-05
updated: 2026-04-05
---

# Linux audit 审计系统

Linux audit 系统记录安全相关事件，用于合规性审计和入侵检测。

## 架构

```
内核审计子系统 → auditd 守护进程 → /var/log/audit/audit.log
                                  → aureport / ausearch（分析工具）
```

## 基本操作

```bash
# 服务管理
systemctl enable --now auditd
systemctl status auditd

# 查看状态
auditctl -s                    # 审计系统状态
auditctl -l                    # 列出所有规则
auditctl -l | wc -l            # 规则数量
```

## 添加审计规则

```bash
# 监控文件访问
auditctl -w /etc/passwd -p wa -k passwd_change
auditctl -w /etc/shadow -p wa -k shadow_change

# 监控目录（递归）
auditctl -w /var/www/ -p wa -k web_changes

# 监控系统调用
auditctl -a always,exit -F arch=b64 -S execve -k exec_log
auditctl -a always,exit -F arch=b64 -S connect -k network_log

# 按用户审计
auditctl -a always,exit -F uid=1000 -k user_alice

# -p 权限: r(读) w(写) x(执行) a(属性变更)
# -k 审计关键字（用于搜索）
```

## 查询审计日志

```bash
# 按关键字搜索
ausearch -k passwd_change
ausearch -k passwd_change --start today
ausearch -f /etc/passwd              # 按文件名

# 报告
aureport --summary                   # 综合报告
aureport --auth                      # 认证事件
aureport --login                     # 登录报告
aureport --file --start 04/01/2026   # 文件访问报告

# 实时监控
tail -f /var/log/audit/audit.log
```

## 持久化规则

```bash
# /etc/audit/rules.d/custom.rules
-w /etc/passwd -p wa -k passwd_change
-w /etc/shadow -p wa -k shadow_change
-a always,exit -F arch=b64 -S execve -k exec_log

# 重新加载
augenrules --load
```

## 关联
- [[linux-sudo-与提权机制]] — 审计 sudo 操作
- [[linux-SELinux-与-AppArmor]] — SELinux 使用审计日志记录拒绝

## 关键结论

> audit 系统是合规性（等保、PCI-DSS、SOC2）的基础：记录"谁在什么时候做了什么"。生产服务器必须开启 auditd 并配置关键文件监控。
