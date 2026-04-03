---
title: "GDT 与段描述符"
tags: [x86, hardware, GDT, segment]
aliases: ["Global Descriptor Table", "段描述符表"]
created: 2026-04-03
updated: 2026-04-03
---

# GDT 与段描述符

GDT（Global Descriptor Table）是 x86 保护模式的核心数据结构，定义内存段的基址、界限和访问权限。

## 段描述符（8 字节）

```
 63       56 55  52 51  48 47       40 39       16 15        0
┌──────────┬──────┬──────┬───────────┬───────────┬───────────┐
│ Base     │Flags │Limit │  Access   │   Base    │  Limit    │
│ 31:24    │ GDBL │ 19:16│  (8 bits) │  23:0     │  15:0     │
└──────────┴──────┴──────┴───────────┴───────────┴───────────┘
```

### Access 字节

```
  7   6  5  4   3   2  1  0
┌───┬────┬───┬───┬────┬────┐
│ P │DPL │ S │ E │DC  │ RW │ A  │
└───┴────┴───┴───┴────┴────┘
P:   存在位
DPL: 特权级 (0-3)
S:   1=代码/数据, 0=系统段
E:   1=可执行(代码), 0=数据
DC:  方向/一致位
RW:  可读(代码)/可写(数据)
A:   已访问
```

## xv6 的 GDT 布局

```c
void seginit(void) {
  c->gdt[SEG_KCODE] = SEG(STA_X|STA_R, 0, 0xffffffff, 0);    // 内核代码 DPL=0
  c->gdt[SEG_KDATA] = SEG(STA_W,       0, 0xffffffff, 0);    // 内核数据 DPL=0
  c->gdt[SEG_UCODE] = SEG(STA_X|STA_R, 0, 0xffffffff, DPL_USER); // 用户代码 DPL=3
  c->gdt[SEG_UDATA] = SEG(STA_W,       0, 0xffffffff, DPL_USER); // 用户数据 DPL=3
}
```

关键设计：**基址全为 0，界限全为 0xFFFFFFFF**——即平坦模型（Flat Model），段机制被"架空"，实际靠页表做保护。

## 为什么还需要 GDT？

虽然平坦模型让段基址=0，但 x86 硬件仍然要求：
- 代码段的 DPL 决定 CPL（当前特权级）
- 段选择子区分内核态/用户态
- `int 0x80` 时检查 DPL 决定是否允许陷入

## 关键要点

> xv6 用 GDT 只做一件事：**通过 DPL 区分内核态和用户态**。基址和界限都是满的，真正的内存保护靠页表。这是现代 OS 的标准做法——段机制是 x86 的历史遗留，实际在平坦模型下名存实亡。

## 关联
- [[x86 实模式与保护模式]] — lgdt 加载 GDT
- [[x86 特权级]] — DPL/RPL/CPL 的关系
- [[xv6 启动流程]] — seginit 在 main 中初始化 GDT
- [[xv6 中断与陷阱]] — SETGATE 设置 IDT 时引用 GDT 选择子
