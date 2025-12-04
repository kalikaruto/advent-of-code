file = 'input.txt'
data = None
dial = 50
max_dial = 100
min_dial = 0
count = 0

with open(file) as f:
    data = f.read().strip().split('\n')

for d in data:
    dir = d[0]
    num = int(d[1:])
    if dir == 'L':
        dial -= num
    else:
        dial += num
    dial %= max_dial
    if dial == min_dial:
        count += 1
    print(dial)
print(count)
