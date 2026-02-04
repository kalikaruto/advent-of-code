grid = [list(line.strip()) for line in open("input.txt")]
R, C = len(grid), len(grid[0])

# DP table: dp[r][c] = number of timelines that reach (r,c)
dp = [[0]*C for _ in range(R)]

# source
sr = 0
sc = grid[0].index("S")
dp[sr][sc] = 1

def in_bounds(r, c):
    return 0 <= r < R and 0 <= c < C

for r in range(sr, R-1):        # go row by row downward
    for c in range(C):
        if dp[r][c] == 0:
            continue

        below = r + 1
        if grid[below][c] == '^':
            # split → two independent timelines
            if in_bounds(below, c-1):
                dp[below][c-1] += dp[r][c]
            if in_bounds(below, c+1):
                dp[below][c+1] += dp[r][c]
        else:
            # just fall straight down
            dp[below][c] += dp[r][c]

# sum all timelines that leave the bottom row
answer = sum(dp[R-1])
print(answer)

