---
title: AVL 树
tags: [算法, 数据结构, 树, 自平衡]
aliases: [AVL Tree, 平衡二叉树]
created: 2026-04-04
updated: 2026-04-04
---

# AVL 树

AVL 树是最早的自平衡二叉搜索树，通过旋转操作保证任意节点的左右子树高度差不超过 1。

## 平衡因子

```
balance_factor(node) = height(node.left) - height(node.right)
```

AVL 要求所有节点的 balance_factor ∈ {-1, 0, 1}。

## 四种旋转

### LL 型（左左）— 右旋

```
    z                  y
   / \               /   \
  y   T4    →       x     z
 / \               / \   / \
x   T3            T1 T2 T3 T4
/ \
T1 T2
```

### RR 型（右右）— 左旋

```
z                    y
/ \                 /   \
T1   y      →      z     x
    / \           / \   / \
   T2   x        T1 T2 T3 T4
       / \
      T3 T4
```

### LR 型（左右）— 先左旋再右旋

### RL 型（右左）— 先右旋再左旋

## 旋转实现

```python
class AVLNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.height = 1

def height(node):
    return node.height if node else 0

def balance_factor(node):
    return height(node.left) - height(node.right) if node else 0

def right_rotate(z):
    y = z.left
    T3 = y.right
    y.right = z
    z.left = T3
    z.height = 1 + max(height(z.left), height(z.right))
    y.height = 1 + max(height(y.left), height(y.right))
    return y

def left_rotate(z):
    y = z.right
    T2 = y.left
    y.left = z
    z.right = T2
    z.height = 1 + max(height(z.left), height(z.right))
    y.height = 1 + max(height(y.left), height(y.right))
    return y

def insert(node, val):
    # 1. 标准 BST 插入
    if not node:
        return AVLNode(val)
    if val < node.val:
        node.left = insert(node.left, val)
    elif val > node.val:
        node.right = insert(node.right, val)
    else:
        return node

    # 2. 更新高度
    node.height = 1 + max(height(node.left), height(node.right))

    # 3. 获取平衡因子，判断旋转类型
    bf = balance_factor(node)

    # LL
    if bf > 1 and val < node.left.val:
        return right_rotate(node)
    # RR
    if bf < -1 and val > node.right.val:
        return left_rotate(node)
    # LR
    if bf > 1 and val > node.left.val:
        node.left = left_rotate(node.left)
        return right_rotate(node)
    # RL
    if bf < -1 and val < node.right.val:
        node.right = right_rotate(node.right)
        return left_rotate(node)

    return node
```

## 复杂度

| 操作 | 时间 | 说明 |
|------|------|------|
| 查找 | O(log n) | 树高始终 ≤ 1.44 log₂(n) |
| 插入 | O(log n) | 含旋转，最多 2 次旋转 |
| 删除 | O(log n) | 可能需要 O(log n) 次旋转 |
| 空间 | O(n) | 每节点额外 height 字段 |

## AVL vs 红黑树

| 特性 | AVL | 红黑树 |
|------|-----|--------|
| 平衡标准 | 高度差 ≤ 1 | 路径黑色节点数相同 |
| 查找 | ✅ 更快（更平衡） | 稍慢 |
| 插入/删除 | 旋转较多 | 旋转较少 |
| 适用场景 | 查找密集 | 插入删除频繁 |

## 关键要点

> [!important] AVL 是最严格的自平衡 BST
> 任何节点的子树高度差不超过 1，保证 O(log n)

> [!important] 插入最多 2 次旋转
> LL/RR 只需 1 次，LR/RL 需 2 次

> [!important] 删除可能需要多次旋转
> 从删除点向上回溯，每个祖先都可能需要旋转

## 相关

- [[二叉搜索树]] — AVL 的基础
- [[红黑树]] — 实际工程更常用的自平衡 BST
