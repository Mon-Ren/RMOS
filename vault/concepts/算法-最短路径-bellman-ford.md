---
title: 最短路径 Bellman-Ford
tags: [algorithm, graph, shortest-path]
aliases: [Bellman-Ford, Bellman-Ford算法, 最短路径Bellman-Ford]
created: 2026-04-04
updated: 2026-04-04
---

# 最短路径 Bellman-Ford

Bellman-Ford 算法通过对所有边重复执行松弛操作来求解单源最短路径，支持负权边并能检测负权环。

## 核心思想

对图中所有边执行 **V-1 轮松弛**。每轮扫描所有边 `(u, v)`，若 `dist[u] + w(u,v) < dist[v]`，则更新 `dist[v]`。V-1 轮后所有最短路径确定（最长最短路径至多 V-1 条边）。

**负权环检测**：第 V 轮若仍有边可松弛，说明存在负权环。

## 算法实现

```python
def bellman_ford(V, edges, src):
    dist = [float('inf')] * V
    dist[src] = 0
    
    # V-1 轮松弛
    for i in range(V - 1):
        updated = False
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                updated = True
        if not updated:  # 优化：无更新则提前退出
            break
    
    # 第 V 轮检测负权环
    for u, v, w in edges:
        if dist[u] + w < dist[v]:
            return None  # 存在负权环
    
    return dist
```

## SPFA 优化

SPFA（Shortest Path Faster Algorithm）是 Bellman-Ford 的队列优化版本：

```python
from collections import deque

def spfa(V, adj, src):
    dist = [float('inf')] * V
    dist[src] = 0
    in_queue = [False] * V
    count = [0] * V
    
    q = deque([src])
    in_queue[src] = True
    
    while q:
        u = q.popleft()
        in_queue[u] = False
        for v, w in adj[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                if not in_queue[v]:
                    q.append(v)
                    in_queue[v] = True
                    count[v] += 1
                    if count[v] >= V:  # 负权环
                        return None
    return dist
```

> [!tip] 复杂度分析
> - **时间**：标准 Bellman-Ford O(VE)，SPFA 平均 O(kE)（k 为常数），最坏 O(VE)
> - **空间**：O(V + E)

> [!info] 适用场景
> - 存在负权边时不能用 Dijkstra
> - 需要检测负权环
> - 边数较多且期望提前终止时 SPFA 更快

## 关联

- [[算法-最短路径-dijkstra|最短路径 Dijkstra]] — 无负权边时更高效，O(V² + E) 或 O(E log V)
- [[图的表示]] — 邻接表/邻接矩阵存储
- [[算法-动态规划基础|动态规划基础]] — 松弛操作本质是 DP 的转移
