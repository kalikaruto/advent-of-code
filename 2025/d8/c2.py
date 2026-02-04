from collections import Counter
from math import prod
import itertools

file='input.txt'
def read_points(file):
    pts = []
    with open(file) as f:
        for line in f:
            line=line.strip()
            if not line: continue
            x,y,z = map(int, line.split(','))
            pts.append((x,y,z))
    return pts

def last_connection_x_product(points):
    n = len(points)
    # build all (dsq,i,j)
    pairs = []
    for i,j in itertools.combinations(range(n), 2):
        x1,y1,z1 = points[i]
        x2,y2,z2 = points[j]
        dsq = (x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2
        pairs.append((dsq, i, j))
    pairs.sort(key=lambda x: x[0])

    parent = list(range(n))
    rank = [0]*n
    comp = n

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    def union(a,b):
        nonlocal comp
        ra, rb = find(a), find(b)
        if ra == rb:
            return False
        if rank[ra] < rank[rb]:
            parent[ra] = rb
        else:
            parent[rb] = ra
            if rank[ra] == rank[rb]:
                rank[ra] += 1
        comp -= 1
        return True

    last_i = last_j = None

    for _, i, j in pairs:
        if union(i, j):
            last_i, last_j = i, j
            if comp == 1:
                break

    x1 = points[last_i][0]
    x2 = points[last_j][0]
    return x1 * x2, (points[last_i], points[last_j])


pts = read_points(file)
val, pair = last_connection_x_product(pts)
print("Pair:", pair)
print("X-product:", val)


