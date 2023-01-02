z = []
with open('inputs/input_01.txt','r') as f:
    x = f.read()
    y = x.split("\n\n")
    z = list(map(lambda a: list(map(lambda k: int(k), a.splitlines())), y))
# print(z)
sums = sorted(list(map(lambda a: sum(a), z)))
# print(sums)
print("Answer 1 = ", sums[-1])
print("Answer 2 = ", sum((sorted(sums)[-3:])))

