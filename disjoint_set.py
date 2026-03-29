#!/usr/bin/env python3
"""disjoint_set - Union-Find with path compression and rank."""
import sys

class DisjointSet:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.size = [1] * n
        self.components = n
    
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
        self.size[rx] += self.size[ry]
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        self.components -= 1
        return True
    
    def connected(self, x, y):
        return self.find(x) == self.find(y)
    
    def component_size(self, x):
        return self.size[self.find(x)]
    
    def get_components(self):
        groups = {}
        for i in range(len(self.parent)):
            root = self.find(i)
            if root not in groups:
                groups[root] = []
            groups[root].append(i)
        return list(groups.values())

class WeightedDisjointSet:
    """Union-Find with weighted edges (potential)."""
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.weight = [0] * n  # weight[x] = potential from x to parent[x]
    
    def find(self, x):
        if self.parent[x] == x:
            return x, 0
        root, w = self.find(self.parent[x])
        self.weight[x] += w
        self.parent[x] = root
        return root, self.weight[x]
    
    def union(self, x, y, w):
        """Set potential(y) - potential(x) = w."""
        rx, wx = self.find(x)
        ry, wy = self.find(y)
        if rx == ry:
            return wy - wx == w
        if self.rank[rx] < self.rank[ry]:
            self.parent[rx] = ry
            self.weight[rx] = wy - wx - w
        else:
            self.parent[ry] = rx
            self.weight[ry] = wx - wy + w
            if self.rank[rx] == self.rank[ry]:
                self.rank[rx] += 1
        return True
    
    def diff(self, x, y):
        rx, wx = self.find(x)
        ry, wy = self.find(y)
        if rx != ry:
            return None
        return wy - wx

def test():
    ds = DisjointSet(10)
    assert ds.components == 10
    
    ds.union(0, 1)
    ds.union(2, 3)
    ds.union(0, 2)
    assert ds.connected(0, 3)
    assert not ds.connected(0, 5)
    assert ds.components == 7
    assert ds.component_size(0) == 4
    
    comps = ds.get_components()
    assert any(sorted(c) == [0,1,2,3] for c in comps)
    
    # Weighted
    wds = WeightedDisjointSet(5)
    wds.union(0, 1, 3)   # pot(1) - pot(0) = 3
    wds.union(1, 2, 5)   # pot(2) - pot(1) = 5
    assert wds.diff(0, 2) == 8  # pot(2) - pot(0) = 8
    assert wds.diff(2, 0) == -8
    
    # Contradiction
    assert wds.union(0, 2, 8) == True   # consistent
    assert wds.union(0, 2, 7) == False  # contradicts
    
    print("All tests passed!")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test()
    else:
        print("Usage: disjoint_set.py test")
