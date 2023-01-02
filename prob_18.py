def getInput():
    with open('inputs/input_18.txt', 'r') as f:
        lines = f.read().splitlines()

    lines = [list(map(int, line.split(','))) for line in lines]
    lines = [(line[0], line[1], line[2]) for line in  lines]
    return lines

adj_list = [[0,0,1],[0,0,-1],[0,1,0],[0,-1,0],[1,0,0],[-1,0,0]]


def tup(a):
    return (a[0], a[1], a[2])

def tAdd(a,b):
    return [a[0]+b[0], a[1]+b[1], a[2]+b[2]]

def adjSet(s):
    return list(map(lambda x: tAdd(x, s), adj_list))

def inBound(a,mini,maxi):
    return (a[0] >= mini and a[1] >= mini and a[2] >= mini and 
            a[0] < maxi and a[1] < maxi and a[2] < maxi)

def countFree(mini, maxi, lava):
    frontier = [[mini,mini,mini]]
    seen = set()
    count = 0
    sideCount = 0
    while frontier != []:
        popped = frontier.pop()
        if (tup(popped) in seen):
            continue
        seen.add(tup(popped))
        count += 1
        adjs = adjSet(popped)
        for a in adjs:
            if tup(a) in lava:
                sideCount += 1

        filterAdjs = list(filter(
            lambda x: (inBound(x, mini, maxi) 
                and tup(x) not in seen 
                and tup(x) not in lava), adjs))

        frontier += filterAdjs 

    return sideCount


def part1():
    lines = getInput()
    s = set()
    total = 0
    for l in lines:
        k = adjSet(l)
        s.add(tup(l))
        total += 6
        for i in k:
            if tup(i) in s:
                total -= 2
    print("Answer 1 = ", total)

def part2():
    lines = getInput()
    s = set()
    total = 0
    for l in lines:
        k = adjSet(l)
        s.add(tup(l))
        total += 6
        for i in k:
            if tup(i) in s:
                total -= 2
    sideCount = countFree(-1, 21, s)
    print("Answer 2 = ", sideCount)

part1()
part2()

