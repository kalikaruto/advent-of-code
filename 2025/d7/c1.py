from collections import deque

grid = [list(line.strip()) for line in open("input.txt")]
R, C = len(grid), len(grid[0])

# Find source S
src = (0, grid[0].index('S'))

q = deque([src])
visited = set()
splits = 0

def in_bounds(r, c):
    return 0 <= r < R and 0 <= c < C

while q:
    r, c = q.popleft()
    if (r, c) in visited:
        continue
    visited.add((r, c))

    nr = r + 1
    nc = c

    if not in_bounds(nr, nc):
        continue

    if grid[nr][nc] == '^':
        splits += 1
        # left branch
        if in_bounds(nr, nc-1):
            q.append((nr, nc-1))
        # right branch
        if in_bounds(nr, nc+1):
            q.append((nr, nc+1))
    else:
        # continue down
        q.append((nr, nc))

print(splits)

