import re
import math

def getInput():
    with open('inputs/input_24.txt', 'r') as f:
        lines = f.read().splitlines()
        return lines

def getExample():
    return '''\
#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#'''.splitlines()


def add(t1,t2):
    return (t1[0] + t2[0], t1[1] + t2[1])

ADJS = [(1,0),(0,1),(0,-1),(-1,0),(0,0)]

def adj(i):
    return list(map(lambda x: add(i,x), ADJS))

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

DIR_CHARS = [">","v","<","^"]
def charToDirc(char):
    if char == ">":
        return (1,0)
    elif char == "v":
        return (0,1)
    elif char == "<":
        return (-1,0)
    elif char == "^":
        return (0,-1)
    return (0,0)

def build_bliz_dict(bliz_list):
    bliz_dict = {}
    for bliz in bliz_list:
        point = bliz[0]
        dirc = bliz[1]
        if point in bliz_dict:
            bliz_dict[point] = (dirc,bliz_dict[point][1] + 1)
        else:
            bliz_dict[point] = (dirc,1)
    return bliz_dict
        

def drawMap(wall_set, bliz_list, height, width):
    bliz_dict = build_bliz_dict(bliz_list)
    draw = ""
    for y in range(height):
        for x in range(width):
            if (x,y) in wall_set:
                draw += "#"
            elif (x,y) in bliz_dict:
                bliz = bliz_dict[(x,y)]
                #print(bliz)
                if bliz[1] == 1:
                    draw += dircToChar(bliz[0])
                else:
                    draw += str(bliz[1])
            else:
                draw += '.'
        draw += "\n"
    print(draw)

def getMap(lines):
    wall_set = set()
    start = (0,0)
    end = (0,0)
    bliz_list = []
    bliz_set = set()
    for i in range(len(lines)):
        line = lines[i]
        for j in range(len(line)):
            if line[j] == "#":
                wall_set.add((j,i))
            elif line[j] in DIR_CHARS:
                dirc = charToDirc(line[j])
                # blizzards are unique given both location and direction
                bliz_list.append(((j,i),dirc))
                bliz_set.add((j,i))
            elif line[j] == ".":
                if i == 0:
                    start = (j,i)
                elif i == len(lines)-1:
                    end = (j,i) 
    return wall_set, start, end, len(lines), len(lines[0]), bliz_list, bliz_set

def moveAllBliz(bliz_list, height, width):
    new_list = []
    new_set = set()
    for bliz in bliz_list:
        point = bliz[0]
        dirc = bliz[1]
        new_point = add(point, dirc)
        if new_point[0] <= 0:
            new_point = (width-2, new_point[1]) # one for wall, one because 0 index
        elif new_point[0] >= width-1:
            new_point = (1, new_point[1])
        if new_point[1] <= 0:
            new_point = (new_point[0], height-2)
        elif new_point[1] >= height-1:
            new_point = (new_point[0], 1) 
        new_list.append((new_point,dirc))
        new_set.add(new_point)
    return new_set, new_list

        
def isFreeSquare(wall_set, bliz_set, height, width, point):
    (x,y) = point
    if x < 0 or y < 0 or x >= width or y >= height:
        return False
    if (x,y) in wall_set or (x,y) in bliz_set:
        return False
    return True

def buildTimeGraph(wall_set, bliz_list, bliz_set, height, width):
    time_graph = {}
    rh, rw = height - 2, width - 2
    lcm = (rh*rw)//(math.gcd(rh,rw))

    for t in range(lcm + 1):
        new_bliz_set, new_bliz_list = moveAllBliz(bliz_list, height, width)
        for y in range(height):
            for x in range(width):
                if (x,y) not in wall_set and (x,y) not in bliz_set:
                    adjs = adj((x,y))
                    for a in adjs:
                        if isFreeSquare(wall_set, new_bliz_set, height, width, a):
                            time_graph[(x,y,t)] = time_graph.get((x,y,t), []) + [(a[0],a[1],(t+1) % lcm)]
        bliz_set = new_bliz_set
        bliz_list = new_bliz_list
    return time_graph

def bfs(time_graph, start, end):
    frontier = [start]
    seen = set()
    count = 0
    while(frontier != []):
        count += 1
        new_frontier = []
        for point in frontier:
            points = time_graph.get(point, [])
            for point in points:
                if (point[0],point[1]) == end:
                    return count, point
                if point not in seen:
                    seen.add(point)
                    new_frontier.append(point)
        frontier = new_frontier
        #print(new_frontier)
    print("Found nothing")
    return -1,(-1,-1,-1)
                

def part1():
    lines = getInput()
    #print(lines)
    wall_set, start, end, height, width, bliz_list, bliz_set = getMap(lines)
    #print(height, width)
    #drawMap(wall_set, bliz_list, height, width)
    rh, rw = height - 2, width - 2
    lcm = (rh*rw)//(math.gcd(rh,rw))
    #print(lcm)
    time_graph = buildTimeGraph(wall_set, bliz_list, bliz_set, height, width)
    time, point = bfs(time_graph, (start[0],start[1],0), end)
    print("Answer 1 =", time)

def part2():
    lines = getInput()
    wall_set, start, end, height, width, bliz_list, bliz_set = getMap(lines)
    #print(height, width)
    #drawMap(wall_set, bliz_list, height, width)
    rh, rw = height - 2, width - 2
    lcm = (rh*rw)//(math.gcd(rh,rw))
    #print(lcm)
    time_graph = buildTimeGraph(wall_set, bliz_list, bliz_set, height, width)
    time, point = bfs(time_graph, (start[0],start[1],0), end)
    time2, point2 = bfs(time_graph, point, start)
    time3, point3 = bfs(time_graph, point2, end)
    print("time ot end",time, point)
    print("back to start",time2, point2)
    print("back to end", time3, point3)

    print("Answer 2 =", time + time2 + time3)

part1()
part2()
