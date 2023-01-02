def priority(x):
    if (x.islower()):
        return ord(x) - 96
    elif (x.isupper()):
        return ord(x) - 38

def process(line):
    p1 = line[:(len(line)//2)]
    p2 = line[(len(line)//2):]
    p_score = sum(list(map(lambda k: priority(k), set(p1).intersection(set(p2)))))
    return p_score

with open('inputs/input_03.txt','r') as f:
    z = f.read().splitlines()

total1 = 0
for l in z:
    t = process(l)
    #print(t)
    total1 += t
print("Answer 1 =", total1)

total2 = 0
for i in range(0,len(z),3):
    b1 = z[i]
    b2 = z[i+1]
    b3 = z[i+2]

    k = set(b1).intersection(set(b2)).intersection(set(b3))
    t = sum(list(map(lambda l: priority(l), k)))
    total2 += t

print("Answer 2 =", total2)
