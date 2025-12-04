from collections import deque
file='input.txt'
data = None
rolls = []

with open(file) as f:
    data = [[c for c in l.strip()] for l in f.readlines()]
drs = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]
max_row=len(data)
max_col=len(data[0])

def bfs(mat, max_row, max_col, drs):
    total=0
    def limits(x,y):
        return 0<=x<max_row and 0<=y<max_col
    def isroll(x,y):
        return limits(x,y) and mat[x][y]=='@'

    neigh = [[0]*max_col for _ in range(max_row)]
    for r in range(max_row):
        for c in range(max_col):
            count=0
            if mat[r][c]=='@':
                for (dx,dy) in drs:
                    nx,ny=r+dx,c+dy
                    if isroll(nx,ny):
                        count+=1
                neigh[r][c]=count
    q = deque()
    for r in range(max_row):
        for c in range(max_col):
            if neigh[r][c]<4:
                q.append((r,c))
    while q:
        (r,c)=q.popleft()
        if mat[r][c]!='@':
            continue
        mat[r][c]='x'
        total+=1
        for dx,dy in drs:
            nx,ny=r+dx,c+dy
            if not isroll(nx,ny):
                continue
            neigh[nx][ny]-=1
            if neigh[nx][ny]<4:
                q.append((nx,ny))

    return total

print(bfs(data,max_row,max_col,drs))


