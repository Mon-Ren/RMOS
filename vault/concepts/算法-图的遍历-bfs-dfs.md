---
title: 图的遍历 BFS/DFS
tags: [算法, 图, 遍历, BFS, DFS]
aliases: [广度优先搜索, 深度优先搜索, BFS, DFS]
created: 2026-04-04
updated: 2026-04-04
---

# 图的遍历 BFS/DFS

BFS（广度优先）和 DFS（深度优先）是图遍历的两种基本方式，几乎所有图算法的基础。

## BFS — 广度优先搜索

使用**队列**，逐层扩展，找到无权图的最短路径。

```python
from collections import deque, defaultdict

def bfs(graph, start):
    visited = {start}
    queue = deque([start])
    order = []

    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return order

# 无权图最短路径
def bfs_shortest_path(graph, start, end):
    visited = {start}
    queue = deque([(start, [start])])
    while queue:
        node, path = queue.popleft()
        if node == end:
            return path
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    return None
```

**时间**：O(V+E) | **空间**：O(V)

## DFS — 深度优先搜索

使用**递归或栈**，尽可能深入一条路径，再回溯。

```python
# 递归实现
def dfs(graph, node, visited=None):
    if visited is None:
        visited = set()
    visited.add(node)
    order = [node]
    for neighbor in graph[node]:
        if neighbor not in visited:
            order.extend(dfs(graph, neighbor, visited))
    return order

# 迭代实现
def dfs_iterative(graph, start):
    visited = set()
    stack = [start]
    order = []
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            order.append(node)
            for neighbor in reversed(graph[node]):
                if neighbor not in visited:
                    stack.append(neighbor)
    return order
```

**时间**：O(V+E) | **空间**：O(V)

## BFS vs DFS

| 特性 | BFS | DFS |
|------|-----|-----|
| 数据结构 | 队列 | 递归/栈 |
| 遍历顺序 | 层序 | 深入后回溯 |
| 最短路径 | ✅ 无权图 | ❌ |
| 空间 | O(最大宽度) | O(最大深度) |
| 连通分量 | ✅ | ✅ |
| 环检测 | ✅ | ✅ |
| 拓扑排序 | ✅ (Kahn) | ✅ (后序) |

## 应用

### 连通分量（DFS）

```python
def count_components(n, edges):
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    visited = set()
    count = 0
    for i in range(n):
        if i not in visited:
            dfs(graph, i, visited)
            count += 1
    return count
```

### 环检测（DFS + 三色标记）

```python
# WHITE(0): 未访问, GRAY(1): 正在访问, BLACK(2): 已完成
def has_cycle_directed(graph, n):
    color = [0] * n

    def dfs(u):
        color[u] = 1  # GRAY
        for v in graph[u]:
            if color[v] == 1:   # 遇到 GRAY → 回边 → 有环
                return True
            if color[v] == 0 and dfs(v):
                return True
        color[u] = 2  # BLACK
        return False

    return any(dfs(i) for i in range(n) if color[i] == 0)
```

### 迷宫问题（BFS 求最短路径）

```python
def shortest_path_maze(maze, start, end):
    m, n = len(maze), len(maze[0])
    queue = deque([(start[0], start[1], 0)])
    visited = {(start[0], start[1])}
    directions = [(0,1),(0,-1),(1,0),(-1,0)]

    while queue:
        x, y, dist = queue.popleft()
        if (x, y) == end:
            return dist
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < m and 0 <= ny < n and (nx, ny) not in visited and maze[nx][ny] == 0:
                visited.add((nx, ny))
                queue.append((nx, ny, dist + 1))
    return -1
```

## 复杂度

- **时间**：O(V + E) — 每个顶点和每条边各访问一次
- **空间**：O(V) — visited 集合 + 队列/栈

## 关键要点

> [!important] BFS 找最短路径（无权图）
> 逐层扩展天然保证第一次到达某节点时路径最短

> [!important] DFS 适合路径搜索和连通性
> 回溯能力使其适合组合、排列、迷宫等路径问题

> [!important] visited 集合不可省略
> 无向图不加 visited 会无限循环，有向图用三色标记更精确

## 相关

- [[图的表示]] — BFS/DFS 的底层数据结构
- [[最短路径 Dijkstra]] — BFS 的加权推广
