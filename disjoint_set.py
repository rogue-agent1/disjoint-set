#!/usr/bin/env python3
"""Disjoint set (Union-Find) data structure. Zero dependencies."""

class DisjointSet:
    def __init__(self, n=0):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.count = n

    def make_set(self, x=None):
        if x is None: x = len(self.parent)
        while len(self.parent) <= x:
            self.parent.append(len(self.parent))
            self.rank.append(0)
            self.count += 1
        return x

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry: return False
        if self.rank[rx] < self.rank[ry]: rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]: self.rank[rx] += 1
        self.count -= 1
        return True

    def connected(self, x, y):
        return self.find(x) == self.find(y)

    def components(self):
        groups = {}
        for i in range(len(self.parent)):
            r = self.find(i)
            groups.setdefault(r, []).append(i)
        return list(groups.values())

    def component_count(self): return self.count

if __name__ == "__main__":
    ds = DisjointSet(10)
    ds.union(0, 1); ds.union(2, 3); ds.union(0, 2)
    print(f"Components: {ds.component_count()}")
    print(ds.components())
