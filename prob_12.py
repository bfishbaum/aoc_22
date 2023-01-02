def getInput():
    with open('inputs/input_12.txt','r') as f:
        lines = f.read().splitlines()
        return [list(x) for x in lines]


adj_list = [[0,1],[0,-1],[1,0],[-1,0]]

def tup(a):
    return (a[0], a[1])

def tAdd(a,b):
    return [a[0]+b[0], a[1]+b[1]]

def adjSet(s):
    return list(map(lambda x: tAdd(x, s), adj_list))

def inBound(a, grid):
    return (a[0] < len(grid) and a[1] < len(grid[a[0]]) and 
            a[0] >= 0 and a[1] >= 0)

def bfs(start, end, grid):
    frontier = [start]
    seen = set()
    count = 0
    while frontier != []:
        new_frontier = []
        count += 1
        for f in frontier:
            if (tup(f) in seen):
                continue
            seen.add(tup(f))
            adjs = adjSet(f)
            for adj in adjs:
                if inBound(adj, grid):
                    fv = grid[f[0]][f[1]]
                    av = grid[adj[0]][adj[1]]
                    #print(adj)
                    #print(fv, av)
                    if f == start and (av == 'a' or av == 'b'):
                        new_frontier.append(adj)
                    # same or one later letter
                    elif av == 'E':
                        if fv == 'z' or fv == 'y':
                            return count
                    elif (ord(av)-ord(fv) < 2):
                        new_frontier.append(adj)
                        #print("Sucess: ", fv, av)
        frontier = new_frontier
        #print(frontier)
    return count

def bfsback(start, end, grid):
    frontier = [end]
    seen = set()
    count = 0
    while frontier != []:
        new_frontier = []
        count += 1
        for f in frontier:
            if (tup(f) in seen):
                continue
            seen.add(tup(f))
            adjs = adjSet(f)
            for adj in adjs:
                if inBound(adj, grid):
                    fv = grid[f[0]][f[1]]
                    av = grid[adj[0]][adj[1]]
                    if f == end and (av == 'z' or av == 'y'):
                        new_frontier.append(adj)
                    # same or one later letter
                    elif av == 'S' or av == 'a':
                        if fv == 'a' or fv == 'b':
                            return count
                    elif (ord(fv) - ord(av) < 2):
                        new_frontier.append(adj)
                        #print("Sucess: ", fv, av)
        frontier = new_frontier
        #print(frontier)
    return count


def part1():
    lines = getInput()
    start = (0,0)
    end = (0,0)
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            if lines[i][j] == "S":
                start = (i,j)
            if lines[i][j] == "E":
                end = (i,j)

    count = bfs(start, end, lines)
    print("Answer 1 =", count)

def part2():
    lines = getInput()
    start = (0,0)
    end = (0,0)
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            if lines[i][j] == "S":
                start = (i,j)
            if lines[i][j] == "E":
                end = (i,j)

    count = bfsback(start, end, lines)
    print("Answer 2 =", count)

part1()
part2()
