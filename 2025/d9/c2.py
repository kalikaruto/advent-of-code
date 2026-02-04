# sparse, width-aware compression solution for AoC Day 9 Part 2
# - works when coordinates are large (e.g. ~1e6)
# - memory ~ O(Vx * Vy) where Vx/Vy ~ number of distinct segment endpoints (<< span)
# - correct tile-based interior/flood-fill and weighted prefix sums

from collections import deque

file = "input.txt"

def read_points(file):
    pts = []
    with open(file) as f:
        for line in f:
            x,y = map(int, line.strip().split(','))
            pts.append((x,y))
    return pts

pts = read_points(file)
n = len(pts)

# gather coordinate keys for compression
xs = set()
ys = set()

# include endpoints and endpoint+1 so intervals map exactly to integer tile columns/rows.
for (x,y) in pts:
    xs.add(x)
    xs.add(x+1)
    ys.add(y)
    ys.add(y+1)

# also include for each segment the opposite endpoint+1 so ranges fully covered
for i in range(n):
    x1,y1 = pts[i]
    x2,y2 = pts[(i+1) % n]
    if x1 == x2:
        # vertical: include y range endpoints and +1
        lo, hi = min(y1,y2), max(y1,y2)
        ys.add(lo)
        ys.add(hi+1)
        xs.add(x1)
        xs.add(x1+1)
    else:
        # horizontal: include x range endpoints and +1
        lo, hi = min(x1,x2), max(x1,x2)
        xs.add(lo)
        xs.add(hi+1)
        ys.add(y1)
        ys.add(y1+1)

# also add outside padding coordinates to allow outside flood from an extra border
xmin = min(x for x,_ in pts)
xmax = max(x for x,_ in pts)
ymin = min(y for _,y in pts)
ymax = max(y for _,y in pts)
xs.add(xmin - 1); xs.add(xmax + 2)
ys.add(ymin - 1); ys.add(ymax + 2)

# sort and build arrays of coordinates (these are the grid boundaries)
xs = sorted(xs)
ys = sorted(ys)

# mapping from coordinate value to index in boundary array
x_to_i = {x:i for i,x in enumerate(xs)}
y_to_j = {y:j for j,y in enumerate(ys)}

# compressed cells are intervals between consecutive boundaries:
# nx = len(xs)-1 columns, ny = len(ys)-1 rows
nx = len(xs) - 1
ny = len(ys) - 1

# grid cell (r,c) corresponds to original x in [xs[c], xs[c+1]) and y in [ys[r], ys[r+1])
# we'll build blocked/allowed map: cell_allowed[r][c] = 1 if cell is red/green (after flood-fill)
cell_allowed = [[0]*nx for _ in range(ny)]

# helper: mark cells covered by a vertical segment at x = X, y in [lo..hi] inclusive
def mark_vertical(x, lo, hi):
    c = x_to_i[x]  # this is column index of boundary; the column for cells that contain x is c
    # cells that have x in their x-interval: those with xs[c] == x
    # Now find rows j where the cell y-interval [ys[j], ys[j+1]) intersects integer y tiles lo..hi.
    j0 = y_to_j[lo]
    j1 = y_to_j[hi+1]  # exclusive
    for j in range(j0, j1):
        # column index for cell is c (because xs[c] == x)
        if 0 <= c < nx and 0 <= j < ny:
            cell_allowed[j][c] = 1

# helper: mark cells covered by a horizontal segment at y = Y, x in [lo..hi] inclusive
def mark_horizontal(y, lo, hi):
    r = y_to_j[y]
    i0 = x_to_i[lo]
    i1 = x_to_i[hi+1]
    for i in range(i0, i1):
        if 0 <= i < nx and 0 <= r < ny:
            cell_allowed[r][i] = 1

# rasterize boundary segments (mark boundary cells allowed)
for i in range(n):
    x1,y1 = pts[i]
    x2,y2 = pts[(i+1) % n]
    if x1 == x2:
        lo, hi = sorted((y1, y2))
        mark_vertical(x1, lo, hi)
    else:
        lo, hi = sorted((x1, x2))
        mark_horizontal(y1, lo, hi)

# flood-fill outside using the padded compressed grid:
# We'll create ext grid with 0 = unknown, 1 = blocked (boundary/allowed), 2 = outside reached
pad_nx = nx + 2
pad_ny = ny + 2
ext = [[0]*pad_nx for _ in range(pad_ny)]  # padded grid indices: (r+1, c+1) maps to cell_allowed[r][c]

# copy blocked cells into ext as 1
for r in range(ny):
    for c in range(nx):
        if cell_allowed[r][c] == 1:
            ext[r+1][c+1] = 1

# BFS from padded corner (0,0)
dq = deque()
dq.append((0,0))
ext[0][0] = 2
while dq:
    pr, pc = dq.popleft()
    for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
        nr, nc = pr+dr, pc+dc
        if 0 <= nr < pad_ny and 0 <= nc < pad_nx and ext[nr][nc] == 0:
            ext[nr][nc] = 2
            dq.append((nr,nc))

# any padded cell with ext == 0 is interior (not reachable from outside).
# mark corresponding compressed cells as allowed as well.
for r in range(ny):
    for c in range(nx):
        if ext[r+1][c+1] == 0:
            cell_allowed[r][c] = 1

# build weighted prefix sums: weight of cell = width * height (# original tiles)
widths = [xs[i+1] - xs[i] for i in range(nx)]
heights = [ys[j+1] - ys[j] for j in range(ny)]

# weighted grid
Wgrid = [[cell_allowed[r][c] * (widths[c] * heights[r]) for c in range(nx)] for r in range(ny)]

# prefix sum ps with shape (ny+1) x (nx+1)
ps = [[0]*(nx+1) for _ in range(ny+1)]
for r in range(ny):
    row_sum = 0
    for c in range(nx):
        row_sum += Wgrid[r][c]
        ps[r+1][c+1] = ps[r][c+1] + row_sum

def rect_weight_sum(ci0, ri0, ci1, ri1):
    # inclusive compressed column indices [ci0..ci1], row indices [ri0..ri1]
    return ps[ri1+1][ci1+1] - ps[ri0][ci1+1] - ps[ri1+1][ci0] + ps[ri0][ci0]

# Prepare lookups to convert original integer rectangle to compressed cell index ranges:
# For original rectangle x in [xa..xb] inclusive (integer tiles), we want compressed columns
# whose x-intervals lie within [xa, xb+1) in terms of boundary coordinates.
# Since we included both x and x+1 for endpoints, the mapping is:
#   ci0 = x_to_i[xa]
#   ci1 = x_to_i[xb+1] - 1
# same for y: ri0 = y_to_j[ya]; ri1 = y_to_j[yb+1] - 1

best = 0
for i in range(n):
    x1,y1 = pts[i]
    for j in range(i+1, n):
        x2,y2 = pts[j]
        xa, xb = sorted([x1, x2])
        ya, yb = sorted([y1, y2])

        # compressed indices
        ci0 = x_to_i[xa]
        ci1 = x_to_i[xb+1] - 1
        ri0 = y_to_j[ya]
        ri1 = y_to_j[yb+1] - 1

        # sanity: indices should be valid ranges
        if ci0 > ci1 or ri0 > ri1:
            continue

        # weighted area expected (in original tiles)
        area = (xb - xa + 1) * (yb - ya + 1)

        # sum of allowed tiles within that compressed rectangle
        allowed_tiles = rect_weight_sum(ci0, ri0, ci1, ri1)

        if allowed_tiles == area and area > best:
            best = area

print(best)

