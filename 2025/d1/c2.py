import operator
file = 'input.txt'
data = None
dial = 50
max_dial = 100
min_dial = 0
count = 0
prev=None
with open(file) as f:
    data = f.read().strip().split('\n')

dial = 50
count = 0

for line in data:
    d = line[0]
    n = int(line[1:])
    step = 1 if d == 'R' else -1

    for _ in range(n):
        dial = (dial + step) % 100
        if dial == 0:
            count += 1

print(count)


