---
title: "Linux udev 设备管理"
tags: [linux, udev, device, rule, hotplug]
aliases: [udev, udev规则, 设备管理, 热插拔, udevadm]
created: 2026-04-05
updated: 2026-04-05
---

# Linux udev 设备管理

udev 是 Linux 的设备管理器，负责在设备热插拔时创建/删除 /dev 设备节点并执行规则。

## 工作流程

```
内核检测到设备 → 发送 uevent → udev 接收
→ 匹配规则 → 创建设备节点 → 设置权限/符号链接 → 执行 RUN 命令
```

## 规则文件

```
/etc/udev/rules.d/       ← 自定义（优先）
/usr/lib/udev/rules.d/   ← 系统默认
```

## 规则语法

```bash
# 匹配条件
SUBSYSTEM=="block", KERNEL=="sd[a-z]", ...
ATTR{idVendor}=="1a86", ATTR{idProduct}=="7523", ...
ENV{ID_BUS}=="usb", ...

# 动作
SYMLINK+="mydevice"              # 创建符号链接
MODE="0666"                      # 设置权限
OWNER="alice", GROUP="devs"     # 设置所有者
RUN+="/usr/local/bin/handle.sh"  # 执行命令
ENV{MY_VAR}="value"             # 设置环境变量
```

## 常用示例

```bash
# USB 串口设备固定名称
# /etc/udev/rules.d/99-serial.rules
SUBSYSTEM=="tty", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="7523", \
    SYMLINK+="arduino", MODE="0666"

# USB 存储设备挂载后执行脚本
# /etc/udev/rules.d/99-usb-mount.rules
ACTION=="add", SUBSYSTEM=="block", ENV{ID_BUS}=="usb", \
    RUN+="/usr/local/bin/mount-usb.sh %k"

# 网卡命名（MAC 绑定）
# /etc/udev/rules.d/70-persistent-net.rules
SUBSYSTEM=="net", ACTION=="add", ATTR{address}=="aa:bb:cc:dd:ee:ff", NAME="wan"
```

## 调试

```bash
# 查看设备属性
udevadm info -a -n /dev/sda
udevadm info -a -n /dev/ttyUSB0

# 测试规则匹配
udevadm test /sys/class/tty/ttyUSB0

# 监控事件
udevadm monitor --property

# 重载规则
udevadm control --reload-rules
udevadm trigger
```

## 关联
- [[linux-sysfs-与设备模型]] — sysfs 提供设备属性
- [[linux-内核模块管理]] — 驱动加载触发 udev

## 关键结论

> udev 规则的关键词匹配是 AND 关系（同一行），同一规则文件的不同行是按顺序执行。自定义规则应放在 /etc/udev/rules.d/ 并用 99- 前缀确保最后执行。
