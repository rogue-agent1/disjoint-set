#!/usr/bin/env python3
"""disjoint_set - Union-Find with path compression and union by rank."""
import sys

class DisjointSet:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.count = n
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
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

def test():
    ds = DisjointSet(6)
    assert ds.count == 6
    ds.union(0, 1)
    ds.union(2, 3)
    ds.union(0, 2)
    assert ds.connected(1, 3)
    assert not ds.connected(0, 4)
    assert ds.count == 3
    comps = ds.components()
    assert len(comps) == 3
    big = max(comps, key=len)
    assert sorted(big) == [0, 1, 2, 3]
    print("OK: disjoint_set")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test()
    else:
        print("Usage: disjoint_set.py test")
