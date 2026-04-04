---
title: Trie 字典树
tags: [algorithm, trie, tree, string, data-structure]
aliases: [Trie, 字典树, 前缀树, Prefix Tree]
created: 2026-04-04
updated: 2026-04-04
---

# Trie 字典树

Trie（又称前缀树/字典树）是一种树形数据结构，用于高效存储和检索字符串集合，支持前缀匹配。

## 结构

每个节点包含：
- 子节点数组（或哈希表）
- 是否为某个字符串的结尾标记

```
       root
      / | \
     a  b  c
    /     |
   p      a
  / \     |
 p   p   t  ← "cat" 结束
 |      
 l      
 e      ← "apple" 结束
```

## 实现

```python
class TrieNode:
    __slots__ = ['children', 'is_end']
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True
    
    def search(self, word: str) -> bool:
        node = self._find(word)
        return node is not None and node.is_end
    
    def starts_with(self, prefix: str) -> bool:
        return self._find(prefix) is not None
    
    def _find(self, prefix: str):
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node
```

## 用数组加速（固定字符集）

```python
class TrieArray:
    def __init__(self):
        self.next = [[-1] * 26]  # next[i][c] = 节点 i 经字符 c 到达的节点
        self.is_end = [False]
    
    def insert(self, word):
        node = 0
        for ch in word:
            c = ord(ch) - ord('a')
            if self.next[node][c] == -1:
                self.next[node][c] = len(self.next)
                self.next.append([-1] * 26)
                self.is_end.append(False)
            node = self.next[node][c]
        self.is_end[node] = True
```

## 压缩 Trie（Radix Tree / Patricia Tree）

将单链路径合并为一条边，减少节点数：

```
普通 Trie:  r - o - o - m
压缩 Trie:  r - "oom"  (一条边存储 "oom")
```

> [!tip] 复杂度分析
> - **插入/查找/前缀匹配**：O(m)，m = 字符串长度
> - **空间**：O(Σ|S_i| · |Σ|)，Σ 为字符集大小
> - 数组实现空间固定 O(节点数 × |Σ|)，哈希实现更省但略慢

> [!info] 应用场景
> - 搜索引擎自动补全
> - 拼写检查
> - IP 路由最长前缀匹配
> - 词频统计
> - 字符串排序

## 关联

- [[算法-哈希表|哈希表]] — 哈希也能做前缀匹配但效率不同
- [[算法-字符串匹配-kmp|KMP]] — 单模式匹配，Trie 适合多模式
- [[算法-滑动窗口|滑动窗口]] — 字符串处理的另一利器
