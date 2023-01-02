def getInput():
    with open('inputs/input_20.txt','r') as f:
        lines = list(map(int, f.read().splitlines()))
        return lines


# lowest positive modulo
def lpm(a,m):
    return a % m 

def newLocation(index, val, length):
    return lpm(val + index, length)

def move(l, moveTo, moveFrom):
    x = l.pop(moveFrom)
    if (moveTo == 0):
        l.append(x)
    else:
        l.insert(moveTo, x)
    return l

def shiftIt(current, toShift):
    l = len(current)
    idx = current.index(toShift)
    if (idx == -1):
        print("nothing there", toShift)
        return current
    item = current[idx]
    newLoc = newLocation(idx, item[0], l-1)
    #print("Shifting: ", item, "from index ", idx, "to", newLoc, "length", l)
    move(current, newLoc, idx)

def shiftFull(current, base):
    for x in base:
        shiftIt(current, x)

def shiftXTimes(current, base, x):
    for i in range(x):
        shiftFull(current, base)

def part1():
    lines = getInput()
    rlines = [(lines[i],i) for i in range(len(lines))]
    shifted = rlines.copy()
    #print(lines)
    #print(shifted)
    shiftXTimes(shifted, rlines, 10)

    idx = 0
    for i in range(len(lines)):
        if shifted[i][0] == 0:
            idx = i
            #print(shifted[i])
            break

    #print(idx)
    v1 = shifted[(idx + 1000) % len(shifted)]
    v2 = shifted[(idx + 2000) % len(shifted)] 
    v3 = shifted[(idx + 3000) % len(shifted)] 
    print("Answer 1 = ", v1[0]+v2[0]+v3[0])

def part2():
    lines = getInput()
    key = 811589153
    lines = list(map(lambda x: x * key, lines))
    rlines = [(lines[i],i) for i in range(len(lines))]
    shifted = rlines.copy()
    #print(lines)
    #print(shifted)
    shiftXTimes(shifted, rlines, 10)

    idx = 0
    for i in range(len(lines)):
        if shifted[i][0] == 0:
            idx = i
            #print(shifted[i])
            break

    #print(idx)
    v1 = shifted[(idx + 1000) % len(shifted)]
    v2 = shifted[(idx + 2000) % len(shifted)] 
    v3 = shifted[(idx + 3000) % len(shifted)] 
    print("Answer 2 = ", v1[0]+v2[0]+v3[0])

part1()
part2()
