file = 'input.txt'

def read_points(file):
    pts = []
    with open(file) as f:
        for line in f:
            x, y = map(int, line.strip().split(','))
            pts.append((x, y))
    return pts

def biggest_rect(pts):
    best = 0
    n = len(pts)
    for i in range(n):
        x1, y1 = pts[i]
        for j in range(i+1, n):
            x2, y2 = pts[j]
            w = abs(x1 - x2) + 1
            h = abs(y1 - y2) + 1
            area = w * h
            if area > best:
                best = area
    return best

pts = read_points(file)
print(biggest_rect(pts))

