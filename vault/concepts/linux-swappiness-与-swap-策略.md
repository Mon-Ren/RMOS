---
title: "Linux swappiness 与 swap 策略"
tags: [linux, swap, swappiness, memory, 调优]
aliases: [swappiness, swap调优, 交换策略, vm.swappiness]
created: 2026-04-05
updated: 2026-04-05
---

# Linux swappiness 与 swap 策略

swappiness 控制内核将匿名内存换出到 swap 的倾向，合理配置对性能影响巨大。

## swappiness 参数

```
值范围: 0-200（默认 60）

0    → 尽量不使用 swap（有内存压力时仍会用）
1    → 最小化 swap
10   → 推荐数据库服务器
60   → 默认值（均衡）
100  → 积极使用 swap
```

```bash
# 查看
cat /proc/sys/vm/swappiness

# 临时修改
sysctl vm.swappiness=10

# 持久化
echo "vm.swappiness=10" >> /etc/sysctl.conf
sysctl -p
```

## 不同场景建议

| 场景 | 建议值 | 原因 |
|------|--------|------|
| 数据库 | 1-10 | 避免换出热点数据 |
| 桌面 | 60 | 默认平衡 |
| 内存充足的服务器 | 10 | 尽量用 RAM |
| 嵌入式 | 0-10 | Flash 寿命 |

## swap 与内存压力

```bash
# 监控 swap 使用
free -h
vmstat 1          # si/so 列
sar -W 1          # swap in/out 统计

# 什么在用 swap
for pid in /proc/[0-9]*/; do
    name=$(cat $pid/comm 2>/dev/null)
    swap=$(grep VmSwap $pid/status 2>/dev/null | awk '{print $2}')
    echo "$pid $name ${swap:-0} kB"
done | sort -k3 -rn | head -20
```

## cgroup v2 swap 控制

```bash
# memory.swap.max：cgroup 的 swap 限制
echo "512M" > /sys/fs/cgroup/myapp/memory.swap.max

# memory.swap.current：当前 swap 使用
cat /sys/fs/cgroup/myapp/memory.swap.current
```

## 关联
- [[linux-内存管理基础]] — free/swap/OOM 基础
- [[linux-cgroup-资源限制]] — cgroup 内存限制

## 关键结论

> swappiness=0 不等于"禁止 swap"，只是极小化倾向。数据库服务器应设为 1-10，避免热点数据被换出导致延迟抖动。swap 最终是安全网，不是性能优化手段。
