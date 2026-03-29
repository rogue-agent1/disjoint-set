from disjoint_set import DisjointSet
ds = DisjointSet(10)
assert ds.component_count() == 10
ds.union(0, 1)
assert ds.connected(0, 1)
assert not ds.connected(0, 2)
assert ds.component_count() == 9
ds.union(2, 3); ds.union(0, 2)
assert ds.connected(0, 3)
assert ds.component_count() == 7
comps = ds.components()
found = [c for c in comps if 0 in c]
assert len(found) == 1
assert set(found[0]) == {0, 1, 2, 3}
# Dynamic make_set
ds.make_set(15)
assert not ds.connected(0, 15)
print("disjoint_set tests passed")
