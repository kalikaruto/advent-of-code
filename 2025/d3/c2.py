file='input.txt'

data=None
banks=[]

with open(file) as f:
    data = [[c for c in l.strip()] for l in f.readlines()]
n = 12

for d in data:
    a = 0
    bank = []
    for i in range(n):
        upper = len(d) - (n - len(bank)) + 1
        a=d.index(max(d[a:upper]), a)
        bank.append(d[a])
        a+=1
    banks.append(''.join(bank))
print(sum([int(n) for n in banks]))


