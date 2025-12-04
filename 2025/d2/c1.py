file='input.txt'
data = None
ranges = []
invalids = []
with open(file) as f:
    data = f.read().strip().split(',')

for d in data:
    ranges.append(list(map(int,d.split('-'))))

for l,u in ranges:
    for i in range(l,u+1):
        s = str(i)
        a,b = s[:len(s)//2],s[len(s)//2:]
        if a == b:
            invalids.append(i)

print(sum(invalids))
