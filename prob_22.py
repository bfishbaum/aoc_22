import re
import math
import time

def getInput():
    with open('inputs/input_22.txt', 'r') as f:
        [a,b] = f.read().split('\n\n')
        return a.rstrip(), b.strip()

def add(t1,t2):
    return (t1[0] + t2[0], t1[1] + t2[1])

def getScore(loc, dirc):
    a = 1000*(loc[1]+1)
    b = 4 * (loc[0]+1)
    c = 0
    if dirc == (1,0):
        c = 0
    elif dirc == (0,1):
        c = 1
    elif dirc == (-1,0):
        c = 2
    elif dirc == (0,-1):
        c = 3
    print(a,"+",b,"+",c, "=", a + b + c)
    return a + b + c

        

def parseInstructions(instructions):
    numre = "[0-9]+"
    n = re.findall(numre, instructions)

    lrre = "[LR]"
    l = re.findall(lrre, instructions)
    return list(map(int, n)),l

def updateMinMaxDict(mmdx,mmdy,x,y):
    if y in mmdy:
        if x < mmdy[y][0]:
            mmdy[y] = (x, mmdy[y][1])
        elif x > mmdy[y][1]:
            mmdy[y] = (mmdy[y][0], x)
    else:
        mmdy[y] = (x,x)
    if x in mmdx:
        if y < mmdx[x][0]:
            mmdx[x] = (y, mmdx[x][1])
        elif y > mmdx[x][1]:
            mmdx[x] = (mmdx[x][0], y)
    else:
        mmdx[x] = (y,y)

def parseMap(graph):
    mmdx = {}
    mmdy = {}
    lines = graph.splitlines()
    outmap = {}
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            if lines[y][x] == ".":
                outmap[(x,y)] = 0
                updateMinMaxDict(mmdx, mmdy, x, y)
            elif lines[y][x] == "#":
                outmap[(x,y)] = 1
                updateMinMaxDict(mmdx, mmdy, x, y)
    return outmap, mmdx, mmdy

def changeDirection(x,y,change):
    if change == "L":
        return (y,-x)
    if change == "R":
        return (-y, x)
    print("Bad change value")
    return (x,y)


def checkNextMove(loc, dirc, graph, mmdx, mmdy):
    new_loc = add(loc,dirc)
    if (dirc[0] != 0 and dirc[1] != 0) or (dirc[0] == 0 and dirc[1] == 0):
        print("error bad direction", dirc)
        return False, (0,0)
    if dirc[0] == 0:
        if new_loc[1] < mmdx[new_loc[0]][0]:
            new_loc = (new_loc[0],mmdx[new_loc[0]][1])
        elif new_loc[1] > mmdx[new_loc[0]][1]:
            new_loc = (new_loc[0],mmdx[new_loc[0]][0])
    elif dirc[1] == 0:
        if new_loc[0] < mmdy[new_loc[1]][0]:
            new_loc = (mmdy[new_loc[1]][1],new_loc[1])
        elif new_loc[0] > mmdy[new_loc[1]][1]:
            new_loc = (mmdy[new_loc[1]][0],new_loc[1])
    else:
        print("error bad direction", loc, dirc, new_loc)
        return False, (0,0)
    if new_loc in graph:
        if graph[new_loc] == 1:
            return False, loc
        elif graph[new_loc] == 0:
            return True, new_loc
    print("Weird, it's not anywher?", loc, dirc, new_loc)
    return False, (0,0)

def followOneInstruction(loc, dirc, move, graph, mmdx, mmdy):
    path = []
    for x in range(move):
        succ, new_loc = checkNextMove(loc, dirc, graph, mmdx, mmdy)
        loc = new_loc
        if not succ:
            break
        path.append((loc,dirc))
    return new_loc, path

def traverseMap(start, moves, turns, graph, mmdx, mmdy):
    loc = start
    dirc = (1,0) # going right
    path = [(start,dirc)]
    #print(loc, dirc)
    for i in range(len(moves)):
        #print(i)
        new_loc, p = followOneInstruction(loc, dirc, moves[i], graph, mmdx, mmdy)
        path += p
        loc = new_loc
        if i < len(turns):
            dirc = changeDirection(dirc[0],dirc[1], turns[i])
    return loc, dirc, path

COLORS = ['\033[95m',
            '\033[94m',
            '\033[96m',
            '\033[92m',
            '\033[91m',
            '\033[93m',
            '\033[99m']

def dircToChar(dirc):
    if dirc == (1,0):
        return ">"
    elif dirc == (0,1):
        return "v"
    elif dirc == (-1,0):
        return "<"
    elif dirc == (0,-1):
        return "^"
    print("DUmbass", dirc)
    return "K"

def drawGraph(x0,x1,y0,y1,graph,path):
    pathd = {}
    for k in path:
        pathd[k[0]] = k[1]
    draw = "" + COLORS[5]
    for y in range(y0,y1+1):
        draw += "{:03d}".format(y)
        draw += "    "
        for x in range(x0,x1+1):
            if (x,y) in pathd:
                k = dircToChar(pathd[(x,y)])
                draw += COLORS[1]
                draw += k
                draw += COLORS[5]
            elif (x,y) in graph:
                if graph[(x,y)] == 1:
                    draw += "#"
                else:
                    draw += "."
            else:
                draw += " "
        draw += '\n'
    print(draw)

def part1():
    a,b = getInput()
    moves, turns = parseInstructions(b)
    graph, mmdx, mmdy = parseMap(a)
    start = (mmdy[0][0], 0)
    loc, dirc, path = traverseMap(start, moves, turns, graph, mmdx, mmdy)
    #print(loc, dirc)
    print("Answer 1 =", getScore(loc, dirc))
    #print(path)
    #drawGraph(0,150,0,200,graph,path)

part1()

def checkNextMoveCube(loc, dirc, graph, mmdx, mmdy, extras):
    new_loc = add(loc,dirc)
    new_dirc = dirc
    if (dirc[0] != 0 and dirc[1] != 0) or (dirc[0] == 0 and dirc[1] == 0):
        print("error bad direction", dirc)
        return False, loc, dirc
    if dirc[0] == 0:
        if new_loc[1] < mmdx[new_loc[0]][0] or new_loc[1] > mmdx[new_loc[0]][1]:
            new_loc, new_dirc = overTheWall(loc, new_loc, dirc, graph, mmdx, mmdy, extras)
    elif dirc[1] == 0:
        if new_loc[0] < mmdy[new_loc[1]][0] or new_loc[0] > mmdy[new_loc[1]][1]:
            new_loc, new_dirc = overTheWall(loc, new_loc, dirc, graph, mmdx, mmdy, extras)
    else:
        print("error bad direction", loc, dirc, new_loc)
        return False, loc, dirc
    if new_loc in graph:
        if graph[new_loc] == 1:
            return False, loc, dirc
        elif graph[new_loc] == 0:
            return True, new_loc, new_dirc
    print("Weird, it's not anywher?", loc, dirc, new_loc)
    return False, loc, dirc


def followOneInstructionCube(loc, dirc, move, graph, mmdx, mmdy, extras):
    path = []
    for x in range(move):
        succ, new_loc, new_dirc = checkNextMoveCube(loc, dirc, graph, mmdx, mmdy, extras)
        if not succ:
            break
        loc = new_loc
        dirc = new_dirc
        path.append((loc,dirc))
    return new_loc, path, dirc

def traverseMapCube(start, moves, turns, graph, mmdx, mmdy, extras):
    loc = start
    dirc = (1,0) # going right
    path = [(start,dirc)]
    #print(loc, dirc)
    for i in range(len(moves)):
        #print(i)
        loc, p, dirc = followOneInstructionCube(loc, dirc, moves[i], graph, mmdx, mmdy, extras)
        path += p
        if i < len(turns):
            dirc = changeDirection(dirc[0],dirc[1], turns[i])
            path.append(("Turned", turns[i], "next move is", moves[i+1]))
    return loc, dirc, path

def doCube(graph):
    gset = sorted(set(graph.keys()))
    l = len(gset)
    side = math.sqrt(l // 6)
    print(l, side)
    quads = []
    for y in range(6):
        for x in range(6):
            if ((side * x, side * y) in gset):
                quads.append((x,y))
    return (quads, side)

def getQuadrants(loc, new_loc, quads, side_size):
    div_loc = (int(loc[0]//side_size), int(loc[1]//side_size))
    return quads.index(div_loc) + 1


def overTheWall(loc, new_loc, dirc, graph, mmdx, mmdy, extras):
    (x,y) = loc
    (nx, ny) = new_loc
    # quadrant 1

    if x < 100 and x >= 50 and y < 50 and y >= 0:
        # 1 -> 4
        if nx < x:
            new_new_loc = (0, 149 - ny)
            new_dirc = (1,0)
            return (new_new_loc, new_dirc)
        # 1 -> 6
        elif ny < y:
            new_new_loc = (0, 100 + nx)
            new_dirc = (1,0)
            return (new_new_loc, new_dirc)
    # quadrant 2
    if x < 150 and x >= 100 and y < 50 and y >= 0:
        # 2 -> 5
        if nx > x:
            new_new_loc = (99, 149 - ny)
            new_dirc = (-1,0)
            return (new_new_loc, new_dirc)
        # 2 -> 6
        elif ny < y:
            new_new_loc = (x - 100, 199)
            new_dirc = (0,-1)
            return (new_new_loc, new_dirc)
        # 2 -> 3
        elif ny > y:
            new_new_loc = (99 ,x-50)
            new_dirc = (-1,0)
            return (new_new_loc, new_dirc)
    # quadrant 3
    if x < 100 and x >= 50 and y < 100 and y >= 50:
        # 3 -> 2
        if nx > x:
            new_new_loc = (y + 50, 49)
            new_dirc = (0,-1)
            return (new_new_loc, new_dirc)
        # 3 -> 4
        elif nx < x:
            new_new_loc = (y-50, 100)
            new_dirc = (0,1)
            return (new_new_loc, new_dirc)
    # quadrant 4
    if x < 50 and x >= 0 and y >= 100 and y < 150:
        # 4 -> 1
        if nx < x:
            new_new_loc = (50, 149 - y)
            new_dirc = (1,0)
            return (new_new_loc, new_dirc)
        # 4 -> 3
        elif ny < y:
            new_new_loc = (50, 50+x)
            new_dirc = (1,0)
            return (new_new_loc, new_dirc)
    # quadrant 5
    if x < 100 and x >= 50 and y >= 100 and y < 150:
        # 5 -> 2
        if nx > x:
            new_new_loc = (149, 149 - y)
            new_dirc = (-1,0)
            return (new_new_loc, new_dirc)
        # 5 -> 6
        elif ny > y:
            new_new_loc = (49, 100+x)
            new_dirc = (-1,0)
            return (new_new_loc, new_dirc)
    # quadrant 6
    if x < 50 and x >= 0 and y >= 150 and y < 200:
        # 6 -> 1
        if nx < x:
            new_new_loc = (y-100,0)
            new_dirc = (0,1)
            return (new_new_loc, new_dirc)
        # 6 -> 2
        elif ny > y:
            new_new_loc = (100+x, 0)
            new_dirc = (0,1)
            return (new_new_loc, new_dirc)
        # 6 -> 5
        elif nx > x:
            new_new_loc = (y-100, 149)
            new_dirc = (0,-1)
            return (new_new_loc, new_dirc)
    print("SHouldn't get here!", loc, new_loc, dirc)


def part2():
    a,b = getInput()
    moves, turns = parseInstructions(b)
    graph, mmdx, mmdy = parseMap(a)
    #quads, side_size = doCube(graph)
    start = (mmdy[0][0], 0)
    extra = []

    loc, dirc, path = traverseMapCube(start, moves, turns, graph, mmdx, mmdy, extra)

    # turn on to see map of where you went
    #drawGraph(0,150,0,200,graph,path)

    print("Answer 2 =", getScore(loc, dirc))

part2()
