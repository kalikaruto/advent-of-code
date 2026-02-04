import operator
file='input.txt'
operands=[]
operators=[]
with open(file) as f:
    datas=[l.strip().split() for l in f.read().strip().split('\n')]
    operands=[[int(n) for n in data] for data in datas[:-1]]
    operators=[operator.add if o == '+' else operator.mul for o in datas[-1]]

results=[1 if o is operator.mul else 0 for o in operators]
for i in range(len(operands[0])):
    for j in range(len(operands)):
        results[i] = operators[i](results[i],operands[j][i])

print(sum(results))

