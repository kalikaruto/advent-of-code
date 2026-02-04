import operator

with open("input.txt") as f:
    grid = [l.rstrip("\n") for l in f]

H = len(grid)
W = max(len(l) for l in grid)

# identify columns that are completely spaces → separators
sep = [all(grid[r][c] == " " for r in range(H)) for c in range(W)]

problems = []
cur_cols = []

for c in range(W):
    if sep[c]:
        if cur_cols:
            problems.append(cur_cols)
            cur_cols = []
    else:
        cur_cols.append(c)

if cur_cols:
    problems.append(cur_cols)

total = 0

for cols in problems:
    # collect actual columns belonging to the problem
    # bottom row = operator
    op_char = None
    for c in cols:
        ch = grid[-1][c]
        if ch in "+*":
            op_char = ch
            break

    if op_char is None:
        print('unexpected')
        continue

    op = operator.add if op_char == "+" else operator.mul

    nums = []
    for c in cols:
        col_chars = [grid[r][c] for r in range(H-1)]  # exclude bottom operator row
        col_str = "".join(col_chars).strip()
        if col_str:
            nums.append(int(col_str))

    result = nums[0]
    for n in nums[1:]:
        result = op(result, n)

    total += result

print(total)

