file = 'input.txt'
ranges = []
data = None

with open(file) as f:
    data = f.read().strip().split(',')

for d in data:
    ranges.append(list(map(int,d.split('-'))))

def isrep(s):
    l = len(s)
    for i in range(1, l//2+1):
        if l % i == 0:
            if s[:i] * (l//i) == s:
                return True
    return False
invalids = []

for l,u in ranges:
    for i in range(l,u+1):
        if isrep(str(i)):
            invalids.append(i)
print(invalids)
print(sum(invalids))
