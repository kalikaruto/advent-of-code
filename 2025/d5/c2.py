file='input.txt'
data = None
fresh_range = []
with open(file) as f:
    data = f.readlines()
    flag=False
    for l in data:
        if l.strip() == '':
            flag = True
            break
        fresh_range.append(list(map(int,l.strip().split('-'))))
fresh_range.sort()
merged_range = []
merged_range.append(fresh_range[0])
for l,u in fresh_range:
    if merged_range[-1][1] < l:
        merged_range.append([l,u])
    else:
        merged_range[-1][1] = max(merged_range[-1][1],u)
print(merged_range)
total = 0
for l,u in merged_range:
    total += u-l+1
print(total)
# print(fresh_range)
