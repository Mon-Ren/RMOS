---
title: "Linux PAM 认证模块"
tags: [linux, pam, authentication, security, login]
aliases: [PAM, pluggable authentication, 认证模块, pam.d]
created: 2026-04-05
updated: 2026-04-05
---

# Linux PAM 认证模块

PAM（Pluggable Authentication Modules）提供可插拔的认证框架，应用程序通过 PAM 实现灵活的认证策略。

## 核心概念

PAM 将认证分为四种管理组：

| 组 | 用途 |
|----|------|
| auth | 验证用户身份（密码、指纹等） |
| account | 账户检查（是否过期、是否允许登录） |
| session | 会话管理（设置环境、记录日志） |
| password | 密码修改 |

## 配置文件（/etc/pam.d/）

```bash
# /etc/pam.d/su 示例
# type  control  module-path  arguments
auth       sufficient  pam_rootok.so
auth       required    pam_unix.so
account    required    pam_unix.so
session    required    pam_unix.so
```

### control 值

| 值 | 含义 |
|----|------|
| required | 必须通过，失败继续检查 |
| requisite | 必须通过，失败立即返回 |
| sufficient | 通过即足够，跳过后续 |
| optional | 可选，不影响结果 |

## 常见模块

```bash
pam_unix.so      # 标准 Unix 认证（/etc/shadow）
pam_deny.so      # 拒绝所有
pam_permit.so    # 允许所有
pam_wheel.so     # 限制 su 只允许 wheel 组
pam_limits.so    # 资源限制（/etc/security/limits.conf）
pam_faillock.so  # 登录失败锁定
pam_tally2.so    # 登录计数
pam_google_authenticator.so  # TOTP 二步验证
```

## 实用配置

```bash
# 限制 su 只允许 wheel 组
# /etc/pam.d/su
auth required pam_wheel.so use_uid

# 登录失败 5 次锁定 15 分钟
auth required pam_faillock.so preauth deny=5 unlock_time=900
auth required pam_faillock.so authfail deny=5 unlock_time=900

# 资源限制
# /etc/security/limits.conf
*    soft    nofile    65535
*    hard    nofile    65535
```

## 关联
- [[linux-sudo-与提权机制]] — sudo 也使用 PAM 认证
- [[linux-SSH-配置与安全]] — sshd 使用 PAM 验证密码

## 关键结论

> PAM 让认证逻辑与应用解耦：修改 /etc/pam.d/ 配置就能改变 sshd、login、su 等所有程序的认证方式，无需修改程序本身。
