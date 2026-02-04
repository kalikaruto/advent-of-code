file='input.txt'
data = None
fresh_range = []
ing = []
fresh = []
with open(file) as f:
    data = f.readlines()
    flag=False
    for l in data:
        if l.strip() == '':
            flag = True
            continue
        if flag:
            ing.append(int(l.strip()))
        else:
            fresh_range.append(tuple(map(int,l.strip().split('-'))))

# print(fresh_range)
# print(ing)
for l,u in fresh_range:
    i=0
    while i < len(ing):
        if l <= ing[i] <= u:
            fresh.append(ing[i])
            del ing[i]
            continue
        i+=1

# print(fresh)
print(len(fresh))
