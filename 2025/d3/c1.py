file='input.txt'
data = None
banks = []

with open(file,'r') as f:
    data = [[c for c in l.strip()] for l in f.readlines()]

for d in data:
    i=0
    j=1
    for x in range(2,len(d)):
        a = d[i]+d[j]
        b = d[i]+d[x]
        c = d[j]+d[x]
        # print(a,b,c)
        if a <= b:
            if b <= c:
                i=j
                j=x
            else:
                i=i
                j=x
        else:
            if a <= c:
                i=j
                j=x
            else:
                i=i
                j=j
        # print(d[i]+d[j],i,j)
    banks.append((d[i]+d[j]))
print(data)
print(banks)
print(sum([int(b) for b in banks]))


