def getInput():
    with open('inputs/input_23.txt', 'r') as f:
        lines = f.read().splitlines()
        return lines

def getExample():
    return '''\
....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#..
'''.splitlines()

def add(t1,t2):
    return (t1[0] + t2[0], t1[1] + t2[1])

def getBounds(l):
    minx = min(list(l), key=lambda x: x[0])[0]
    maxx = max(list(l), key=lambda x: x[0])[0]
    miny = min(list(l), key=lambda x: x[1])[1]
    maxy = max(list(l), key=lambda x: x[1])[1]
    return minx, maxx, miny, maxy

def drawElves(elfs):
    l = list(elfs)
    minx, maxx, miny, maxy = getBounds(l)
    draw = ""
    for y in range(miny - 1, maxy + 2):
        for x in range(minx - 1, maxx + 2):
            if (x,y) in elfs:
                draw += "#"
            else:
                draw += "."
        draw += "\n"
    print(draw)
    print(minx,maxx,miny,maxy)

ADJS = [(1,1),(1,0),(1,-1),(0,1),(0,-1),(-1,1),(-1,0),(-1,-1)]

def adj(i):
    return list(map(lambda x: add(i,x), ADJS))

def getDirection(elf, elfs, index_shift):
    (x,y) = elf
    adjs = adj(elf)
    o = [a for a in ADJS if add(elf,a) not in elfs]
    if len(o) == 8:
        #print("good here",elf)
        return elf

    n = [k for k in o if k[1] == -1]
    s = [k for k in o if k[1] == 1]
    e = [k for k in o if k[0] == 1]
    w = [k for k in o if k[0] == -1]
    dirs = [(n,(0,-1)),(s,(0,1)),(w,(-1,0)),(e,(1,0))]

    for i in range(len(dirs)):
        idx = (i + index_shift) % len(dirs)
        d = dirs[(i + index_shift) % len(dirs)]
        if len(d[0]) == 3:
            return add(elf, d[1])
    else:
        #print("nothign looks good here",elf,dirs)
        return elf

def doARound(elf_set,idx):
    elfs = list(elf_set)
    count = {}
    new_elfs = {}
    for elf in elfs:
        new = getDirection(elf, elf_set, idx)
        new_elfs[elf] = new
        count[new] = count.get(new, 0) + 1

    for elf in elfs:
        if count[new_elfs[elf]] > 1:
            new_elfs[elf] = elf

    #print(new_elfs)
    return new_elfs


def part1():
    lines = getInput()

    elfs = set()
    for i in range(len(lines)):
        line = lines[i]
        for j in range(len(line)):
            if line[j] == "#":
                elfs.add((j,i))

        
    new_elfs = elfs
    for x in range(10):
        new_elfs_dict = doARound(new_elfs, x % 4)
        result = set(new_elfs_dict.values())
        new_elfs = result
    #drawElves(new_elfs)
    minx, maxx, miny, maxy = getBounds(new_elfs)
    dx,dy= maxx-minx+1, maxy-miny+1
    area = dx * dy

    #print(minx, maxx,dx, miny, maxy,dy)
    #print(dx,dy,"=", area)
    #print("elfs:", len(elfs))
    print("Answer 1 =", area - len(elfs))
    #print(elfs)

def part2():
    lines = getInput()
    #print(lines)

    elfs = set()
    for i in range(len(lines)):
        line = lines[i]
        for j in range(len(line)):
            if line[j] == "#":
                elfs.add((j,i))

    #print("Orig size", len(elfs))
        
    #drawElves(elfs)
    new_elfs = elfs
    x = 0
    print("Give it a minute for part2...")
    while(True):
        new_elfs_dict = doARound(new_elfs, x % 4)
        x += 1
        result = set(new_elfs_dict.values())
        if len(result.difference(new_elfs)) == 0:
            break
        new_elfs = result
        #if x % 10 == 0:
            #drawElves(new_elfs)
    #drawElves(new_elfs)
    minx, maxx, miny, maxy = getBounds(new_elfs)
    dx,dy= maxx-minx+1, maxy-miny+1
    area = dx * dy
    #print(minx, maxx,dx, miny, maxy,dy)
    #print(dx,dy,"=", area)
    #print("elfs:", len(elfs))
    print("Answer 2 =", x)
    #print(elfs)

part1()
part2()
