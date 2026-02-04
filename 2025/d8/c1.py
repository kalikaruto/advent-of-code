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

def product_of_top3_after_k_pairs(points, K=1000):
    n = len(points)
    total_pairs = n*(n-1)//2
    K = min(K, total_pairs)

    # build list of (squared_distance,i,j)
    pairs = []
    for i,j in itertools.combinations(range(n), 2):
        x1,y1,z1 = points[i]
        x2,y2,z2 = points[j]
        dsq = (x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2
        pairs.append((dsq, i, j))
    pairs.sort(key=lambda x: x[0])

    # union-find (path compression + union by rank)
    parent = list(range(n))
    rank = [0]*n
    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a
    def union(a,b):
        ra, rb = find(a), find(b)
        if ra == rb: return False
        if rank[ra] < rank[rb]:
            parent[ra] = rb
        else:
            parent[rb] = ra
            if rank[ra] == rank[rb]:
                rank[ra] += 1
        return True

    # perform unions for the K shortest pairs (skip effect if already same set)
    for _, i, j in pairs[:K]:
        union(i, j)

    # component sizes
    roots = [find(i) for i in range(n)]
    counts = sorted(Counter(roots).values(), reverse=True)

    # ensure at least 3 factors
    while len(counts) < 3:
        counts.append(1)

    return prod(counts[:3]), counts  # product, sorted list of component sizes


pts = read_points(file)
result_product, sizes = product_of_top3_after_k_pairs(pts, K=1000)
print("Top component sizes (desc):", sizes[:10])
print("Product of top 3 sizes:", result_product)

