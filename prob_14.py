def getInput():
    with open('inputs/input_14.txt', 'r') as f:
        chains = f.read().splitlines()
    return list(map(makeChain, chains))

def makeChain(line):
    chunks = line.split('->')
    chunks = list(map(lambda x: list(map(int, x.strip().split(','))), chunks))
    return chunks

def getExampleInput():
    text = '''498,4 -> 498,6 -> 496,6
    503,4 -> 502,4 -> 502,9 -> 494,9'''
    chains = text.splitlines()
    return list(map(makeChain, chains))


def getBounds(chains):
    x = []
    y = []
    for chain in chains:
        for link in chain:
            x.append(link[0])
            y.append(link[1])
    return (min(x), max(x), min(y), max(y))


def fillMapFromChain(cave_map, chain):
    for c in range(len(chain) - 1):
        start = chain[c]
        end = chain[c+1]
        if start[0] == end[0]:
            x = start[0]
            start_1, end_1 = start[1],end[1]
            if start[1] > end[1]:
                start_1, end_1 = end_1, start_1
            for i in range(start_1, end_1+1):
                cave_map.add((x,i))
        elif start[1] == end[1]:
            y = start[1]
            start_0, end_0 = start[0], end[0]
            if start[0] > end[0]:
                start_0, end_0 = end_0, start_0
            for i in range(start_0, end_0+1):
                cave_map.add((i,y))
        else:
            print("Error bad chain ", chain)

def fillMapFromChains(cave_map, chains):
    for chain in chains:
        fillMapFromChain(cave_map, chain)

def simulateSandFalling(cave_map, sand_map, start_location, max_y):
    (x,y) = start_location
    path = []
    while(y <= max_y):
        path.append((x,y))
        new_loc = (x,y+1)
        if new_loc in cave_map or new_loc in sand_map:
            new_loc = (x-1, y+1)
            if new_loc in cave_map or new_loc in sand_map:
                new_loc = (x+1, y+1)
                if new_loc in cave_map or new_loc in sand_map:
                    return True,x,y,path
                else:
                    x += 1
                    y += 1
                    continue
            else:
                x -= 1
                y += 1
                continue
        else:
            y += 1
            continue
    return False,x,y,path

def simulateSandFallingFloor(cave_map, sand_map, start_location, floor):
    (x,y) = start_location
    path = []
    if (x,y) in sand_map:
        return False,x,y,[]
    while(y < floor-1):
        path.append((x,y))
        new_loc = (x,y+1)
        if new_loc in cave_map or new_loc in sand_map:
            new_loc = (x-1, y+1)
            if new_loc in cave_map or new_loc in sand_map:
                new_loc = (x+1, y+1)
                if new_loc in cave_map or new_loc in sand_map:
                    return True,x,y,path
                else:
                    x += 1
                    y += 1
                    continue
            else:
                x -= 1
                y += 1
                continue
        else:
            y += 1
            continue
    return True, x, y, path


def paintCaveMap(bounds, cave_map, sand_map, path):
    (min_x, max_x, min_y, max_y) = bounds
    drawing = ""

    for y in range(min_y, max_y+1):
        for x in range(min_x, max_x+1):
            if (x,y) in cave_map:
                drawing += "#"
            elif (x,y) in sand_map:
                drawing += "o"
            elif (x,y) in path:
                drawing += "~"
            else:
                drawing += "."
        drawing += "\n"

    print(drawing)
    return drawing

def paintCaveMapFloor(bounds, cave_map, sand_map, path):
    (min_x, max_x, min_y, max_y) = bounds
    drawing = ""

    for y in range(min_y, max_y+3):
        for x in range(min_x, max_x+1):
            if (y == max_y + 2):
                drawing += "#"
            if (x,y) in cave_map:
                drawing += "#"
            elif (x,y) in sand_map:
                drawing += "o"
            elif (x,y) in path:
                drawing += "~"
            else:
                drawing += "."
        drawing += "\n"

    print(drawing)
    return drawing


def part1():
    cave_map = set()
    chains = getInput()
    min_x, max_x, min_y, max_y = getBounds(chains)
    # print(min_x, max_x, min_y, max_y)
    fillMapFromChains(cave_map, chains)

    start_location = (500, 0)

    sand_map = set()
    #paintCaveMap((min_x, max_x, 0, max_y), cave_map, sand_map, set())
    count = 0
    path = []
    while (True):
        success, x, y, path = simulateSandFalling(cave_map, sand_map, start_location, max_y)
        if (not success):
            #print(x,y,count)
            break
        else:
            sand_map.add((x,y))
            count += 1
    print("Answer 1 = ", count)

def part2():
    cave_map = set()
    chains = getInput()
    min_x, max_x, min_y, max_y = getBounds(chains)
    # print(min_x, max_x, min_y, max_y)
    fillMapFromChains(cave_map, chains)

    start_location = (500, 0)

    sand_map = set()
    count = 0
    path = []
    while (True):
        success, x, y, path = simulateSandFallingFloor(cave_map, sand_map, start_location, max_y + 2)
        if (not success):
            break
        else:
            sand_map.add((x,y))
            count += 1

        
    print("Answer 2 = ", count)

part1()
part2()

