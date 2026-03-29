#!/usr/bin/env python3
"""Disjoint set (Union-Find) with path compression and union by rank."""
import sys

class DisjointSet:
    def __init__(self, n):
        self.parent = list(range(n)); self.rank = [0] * n; self.size = [1] * n; self.count = n
    def find(self, x):
        if self.parent[x] != x: self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry: return False
        if self.rank[rx] < self.rank[ry]: rx, ry = ry, rx
        self.parent[ry] = rx; self.size[rx] += self.size[ry]
        if self.rank[rx] == self.rank[ry]: self.rank[rx] += 1
        self.count -= 1; return True
    def connected(self, x, y): return self.find(x) == self.find(y)
    def set_size(self, x): return self.size[self.find(x)]
    def num_sets(self): return self.count

def kruskal_mst(n, edges):
    ds = DisjointSet(n); edges = sorted(edges, key=lambda e: e[2])
    mst = []; total = 0
    for u, v, w in edges:
        if ds.union(u, v): mst.append((u, v, w)); total += w
        if len(mst) == n - 1: break
    return mst, total

def main():
    if len(sys.argv) < 2: print("Usage: disjoint_set.py <demo|test>"); return
    if sys.argv[1] == "test":
        ds = DisjointSet(10)
        assert ds.num_sets() == 10
        ds.union(0, 1); ds.union(2, 3); ds.union(0, 2)
        assert ds.connected(0, 3); assert not ds.connected(0, 4)
        assert ds.set_size(0) == 4; assert ds.num_sets() == 7
        # Duplicate union
        assert not ds.union(0, 1)  # already connected
        # Kruskal MST
        edges = [(0,1,4),(0,2,3),(1,2,1),(1,3,2),(2,3,5)]
        mst, total = kruskal_mst(4, edges)
        assert len(mst) == 3; assert total == 6  # 1+2+3
        # Single element
        ds2 = DisjointSet(1); assert ds2.find(0) == 0; assert ds2.num_sets() == 1
        print("All tests passed!")
    else:
        ds = DisjointSet(5)
        ds.union(0, 1); ds.union(3, 4); ds.union(0, 3)
        print(f"Sets: {ds.num_sets()}, 0-4 connected: {ds.connected(0, 4)}")

if __name__ == "__main__": main()
