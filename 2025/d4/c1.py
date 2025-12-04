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

    for r in range(max_row):
        for c in range(max_col):
            count=0
            if mat[r][c]=='@':
                for (dx,dy) in drs:
                    nx,ny=r+dx,c+dy
                    if isroll(nx,ny):
                        count+=1
                if count<4:
                    total+=1
    return total

print(bfs(data,max_row,max_col,drs))

