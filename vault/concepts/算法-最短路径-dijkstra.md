---
title: 最短路径 Dijkstra
tags: [算法, 图, 最短路径, 贪心]
aliases: [Dijkstra, 迪杰斯特拉, 单源最短路径]
created: 2026-04-04
updated: 2026-04-04
---

# 最短路径 Dijkstra

Dijkstra 算法是解决**单源最短路径**的经典贪心算法，适用于所有边权非负的加权图。

## 核心思想

```
1. 维护 dist[] 数组，dist[v] 表示从起点到 v 的当前最短距离
2. 每次从未确定最短距离的节点中选 dist 最小的
3. 用该节点松弛其所有邻居
4. 重复直到所有节点确定
```

> [!warning] 不能处理负权边
> Dijkstra 的贪心前提是"已确定的最短距离不会再变小"，负权边会打破这个假设。

## 朴素实现

```python
import math

def dijkstra_naive(graph, start, n):
    """graph: 邻接表 graph[u] = [(v, weight), ...]"""
    dist = [math.inf] * n
    visited = [False] * n
    dist[start] = 0

    for _ in range(n):
        # 找未访问中 dist 最小的节点 — O(V)
        u = -1
        for i in range(n):
            if not visited[i] and (u == -1 or dist[i] < dist[u]):
                u = i
        if dist[u] == math.inf:
            break
        visited[u] = True

        # 松弛邻居
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w

    return dist
```

**时间**：O(V²) | **空间**：O(V)

## 优先队列优化

```python
import heapq

def dijkstra(graph, start, n):
    dist = [float('inf')] * n
    dist[start] = 0
    heap = [(0, start)]  # (距离, 节点)

    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:   # 跳过已更新的旧条目
            continue
        for v, w in graph[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(heap, (nd, v))

    return dist
```

**时间**：O((V + E) log V) | **空间**：O(V)

> 每个节点最多入堆 O(degree(u)) 次，总入堆 O(E) 次，每次 push/pop O(log V)。

## 记录路径

```python
def dijkstra_with_path(graph, start, n):
    dist = [float('inf')] * n
    parent = [-1] * n
    dist[start] = 0
    heap = [(0, start)]

    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, w in graph[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                parent[v] = u
                heapq.heappush(heap, (nd, v))

    # 还原路径
    def get_path(target):
        path = []
        while target != -1:
            path.append(target)
            target = parent[target]
        return path[::-1]

    return dist, get_path
```

## 与 BFS 的关系

```
BFS = Dijkstra 的特例（所有边权 = 1）

BFS：队列，每次取队首 → 等价于边权全为 1 的 Dijkstra
Dijkstra：优先队列，每次取最小 dist → 通用加权版本
```

| 特性 | BFS | Dijkstra |
|------|-----|----------|
| 边权 | 全为 1 | 非负 |
| 数据结构 | 队列 | 优先队列 |
| 时间 | O(V+E) | O((V+E) log V) |
| 最短路径 | ✅ 无权图 | ✅ 非负权图 |

## 复杂度

| 版本 | 时间 | 空间 |
|------|------|------|
| 朴素（数组） | O(V²) | O(V) |
| 优先队列 | O((V+E) log V) | O(V) |

**适用场景**：
- 稠密图 (E ≈ V²)：朴素 O(V²) 更优
- 稀疏图 (E << V²)：优先队列 O((V+E) log V) 更优

## 关键要点

> [!important] 负权边用 Bellman-Ford
> Dijkstra 的贪心前提被负权破坏，负权边必须用 Bellman-Ford

> [!important] "懒删除"技巧
> 优先队列中可能有同一节点的多个旧距离条目，用 `d > dist[u]` 判断跳过

> [!important] Dijkstra 是 BFS 的推广
> 理解这一点有助于统一图搜索的框架：BFS → Dijkstra → A*

## 相关

- [[图的遍历 BFS/DFS]] — Dijkstra 的无权特例
- [[堆与优先队列]] — Dijkstra 优化的关键数据结构
- [[图的表示]] — Dijkstra 通常用邻接表
