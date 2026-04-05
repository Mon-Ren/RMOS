---
title: "Linux RAID 磁盘阵列"
tags: [linux, raid, storage, mdadm, 冗余]
aliases: [RAID, mdadm, 磁盘阵列, 软RAID, RAID0, RAID1, RAID5]
created: 2026-04-05
updated: 2026-04-05
---

# Linux RAID 磁盘阵列

RAID（Redundant Array of Independent Disks）通过多磁盘组合提供性能提升和数据冗余。

## 常见 RAID 级别

| 级别 | 最少磁盘 | 冗余 | 读性能 | 写性能 | 可用容量 |
|------|----------|------|--------|--------|----------|
| RAID 0 | 2 | ❌ | 高 | 高 | N×min |
| RAID 1 | 2 | ✅ | 高 | 中 | min |
| RAID 5 | 3 | ✅ | 高 | 中 | (N-1)×min |
| RAID 6 | 4 | ✅(2块) | 高 | 低 | (N-2)×min |
| RAID 10 | 4 | ✅ | 高 | 高 | N/2×min |

## mdadm 操作

```bash
# 创建 RAID 5（3 块磁盘）
mdadm --create /dev/md0 --level=5 --raid-devices=3 /dev/sdb /dev/sdc /dev/sdd

# 查看状态
cat /proc/mdstat
mdadm --detail /dev/md0
mdadm --detail --scan

# 格式化和挂载
mkfs.ext4 /dev/md0
mount /dev/md0 /mnt/raid

# 持久化
mdadm --detail --scan >> /etc/mdadm/mdadm.conf
update-initramfs -u

# 替换故障磁盘
mdadm --manage /dev/md0 --fail /dev/sdc     # 标记故障
mdadm --manage /dev/md0 --remove /dev/sdc   # 移除
mdadm --manage /dev/md0 --add /dev/sde      # 添加新磁盘

# 监控
mdadm --monitor --scan --daemonize           # 后台监控
watch cat /proc/mdstat                        # 实时查看
```

## 关联
- [[linux-磁盘与分区管理]] — 基础分区和格式化
- [[linux-LVM-逻辑卷管理]] — 可在 RAID 上构建 LVM

## 关键结论

> RAID 不是备份：RAID 防硬件故障，不防误删和病毒。生产环境应 RAID + 定期备份。
