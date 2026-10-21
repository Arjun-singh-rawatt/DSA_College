"""Small reusable graph algorithms using adjacency dictionaries."""
from collections import deque
import heapq


def bfs(graph, start):
    seen, order, queue = {start}, [], deque([start])
    while queue:
        node = queue.popleft(); order.append(node)
        for neighbor in graph.get(node, ()):
            if neighbor not in seen:
                seen.add(neighbor); queue.append(neighbor)
    return order


def dfs(graph, start):
    seen, order, stack = set(), [], [start]
    while stack:
        node = stack.pop()
        if node in seen: continue
        seen.add(node); order.append(node)
        stack.extend(reversed(list(graph.get(node, ()))))
    return order


def _undirected_edges(graph):
    edges = {}
    for u, neighbors in graph.items():
        for v, weight in neighbors:
            if u == v: continue
            key = frozenset((u, v))
            if key in edges and edges[key] != weight: raise ValueError("Conflicting undirected edge weights")
            edges[key] = weight
    return [(min(e, key=str), max(e, key=str), w) for e, w in edges.items()]


def prim(graph, start=None):
    if not graph: return [], 0
    start = start if start is not None else next(iter(graph))
    if start not in graph: raise ValueError("Start node is not in graph")
    visited, result, total = {start}, [], 0
    heap = [(w, str(start), str(v), start, v) for v, w in graph[start]]
    heapq.heapify(heap)
    while heap and len(visited) < len(graph):
        w, _, _, u, v = heapq.heappop(heap)
        if v in visited: continue
        visited.add(v); result.append((u, v, w)); total += w
        for nxt, weight in graph.get(v, ()):
            if nxt not in visited: heapq.heappush(heap, (weight, str(v), str(nxt), v, nxt))
    if len(visited) != len(graph): raise ValueError("Graph is disconnected")
    return result, total


def kruskal(graph):
    parent = {node: node for node in graph}
    def root(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    result, total = [], 0
    for u, v, w in sorted(_undirected_edges(graph), key=lambda e: e[2]):
        if root(u) != root(v):
            parent[root(u)] = root(v); result.append((u, v, w)); total += w
    if len(result) != max(0, len(graph) - 1): raise ValueError("Graph is disconnected")
    return result, total


def dijkstra(graph, start):
    if start not in graph: raise ValueError("Start node is not in graph")
    if any(w < 0 for edges in graph.values() for _, w in edges): raise ValueError("Dijkstra requires nonnegative weights")
    distances = {n: float("inf") for n in graph}; distances[start] = 0
    heap = [(0, start)]
    while heap:
        distance, node = heapq.heappop(heap)
        if distance != distances[node]: continue
        for neighbor, weight in graph.get(node, ()):
            candidate = distance + weight
            if neighbor not in distances: distances[neighbor] = float("inf")
            if candidate < distances[neighbor]: distances[neighbor] = candidate; heapq.heappush(heap, (candidate, neighbor))
    return distances


def bellman_ford(graph, start):
    nodes = set(graph)
    for u, edges in graph.items():
        for v, _ in edges: nodes.add(v)
    if start not in nodes: raise ValueError("Start node is not in graph")
    edges = [(u, v, w) for u, neighbors in graph.items() for v, w in neighbors]
    dist = {node: float("inf") for node in nodes}; dist[start] = 0
    for _ in range(len(nodes) - 1):
        changed = False
        for u, v, w in edges:
            if dist[u] != float("inf") and dist[u] + w < dist[v]: dist[v] = dist[u] + w; changed = True
        if not changed: break
    if any(dist[u] != float("inf") and dist[u] + w < dist[v] for u, v, w in edges):
        raise ValueError("Reachable negative-weight cycle detected")
    return dist
