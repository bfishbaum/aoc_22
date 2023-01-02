import re
import time
from functools import lru_cache

def parseBlueprint(line):
    numre = '[0-9]+'
    rate = re.findall(numre, line)
    return list(map(int, rate))

def getInput():
    with open('inputs/input_19.txt', 'r') as f:
        lines = f.read().splitlines()
        return lines

#robot_types = ['obs', 'clay', 'obs', 'geo']
robot_types = [0, 1, 2, 3]

def tuple3Add(tuple1, tuple2):
    return (tuple1[0] + tuple2[0],
     tuple1[1] + tuple2[1],
     tuple1[2] + tuple2[2])


def subResources(resources, blueprint, robot_type):
    if robot_type == 0:
        return tuple3Add(resources, (-blueprint[0], 0,0))
    if robot_type == 1:
        return tuple3Add(resources, (-blueprint[1], 0,0))
    if robot_type == 2:
        return tuple3Add(resources, (-blueprint[2][0],-blueprint[2][1],0))
    if robot_type == 3:
        return tuple3Add(resources, (-blueprint[3][0],0,-blueprint[3][1]))

def getRobotsCanBuild(blueprint, resources):
    result = []
    if (blueprint[3][0] <= resources[0] and blueprint[3][1] <= resources[2]):
        result.append(3)
    if (blueprint[2][0] <= resources[0] and blueprint[2][1] <= resources[1]):
        result.append(2)
    if (blueprint[1] <= resources[0]):
        result.append(1)
    if (blueprint[0] <= resources[0]):
        result.append(0)
    return result

speed_up = True

def printPath(path):
    time = 32
    robots = [1,0,0,0]
    geodes = 0
    for x in path:
        print("Minute ", time - x[1])
        print("Robots: ", robots)
        print("Resources: ", x[2], "->", tuple3Add(x[2], robots[:3]))
        print("Geodes: ", geodes)
        if x[0] == -1:
            print("Built no robot")
        else:
            print("Built robot type: ", x[0])
            robots[x[0]] += 1
        geodes += robots[3]
        print('\n')

@lru_cache(maxsize=None)
def calcMaxGeodes(a,b,c,resources, blueprint, time):
    if time <= 0:
        return 0,[]
    else:
        new_resources = tuple3Add(resources, (a,b,c))
        can_build = getRobotsCanBuild(blueprint, resources)
        best = -1
        best_path = []
        if can_build == [] or a < blueprint[4][0]:
            v, p = calcMaxGeodes(a,b,c, new_resources, blueprint, time - 1)
            best = v
            best_path = [(-1, time, resources, can_build)] + p
        for robot_type in can_build:
            val = 0
            path = []
            if robot_type == 0 and a < blueprint[4][0]:
                val,path = calcMaxGeodes(a+1,b,c, subResources(new_resources, blueprint, robot_type), blueprint, time - 1)
            if robot_type == 1 and b < blueprint[4][1]:
                val,path = calcMaxGeodes(a,b+1,c, subResources(new_resources, blueprint, robot_type), blueprint, time - 1)
            if robot_type == 2 and c < blueprint[4][2]:
                val,path = calcMaxGeodes(a,b,c+1, subResources(new_resources, blueprint, robot_type), blueprint, time - 1)
            if robot_type == 3:
                v, path = calcMaxGeodes(a,b,c, subResources(new_resources, blueprint, robot_type), blueprint, time - 1)
                val = (time - 1) + v
            if val > best:
                best = val
                best_path = [(robot_type, time, resources)] + path
        if best == -1:
            print("FUCKED UP AARON")
        return best, best_path



@lru_cache(maxsize=256)
def calcMaxGeodesFixedOre(a,b,c,resources, blueprint, time, fixed_ore):
    if time <= 0:
        return 0,[]
    else:
        new_resources = tuple3Add(resources, (a,b,c))
        if a < fixed_ore: 
            if resources[0] >= blueprint[0]:
                val,path = calcMaxGeodesFixedOre(a+1,b,c, subResources(new_resources, blueprint, 0), blueprint, time - 1, fixed_ore)
                best_path = [(0, time, resources)] + path
                return val, best_path
            else:
                v, p = calcMaxGeodesFixedOre(a,b,c, new_resources, blueprint, time - 1, fixed_ore)
                best = v
                best_path = [(-1, time, resources)] + p
                return best, best_path

        can_build = getRobotsCanBuild(blueprint, resources)
        best = -1
        best_path = []
        if can_build == [] or a < blueprint[4][0]:
            v, p = calcMaxGeodesFixedOre(a,b,c, new_resources, blueprint, time - 1, fixed_ore)
            best = v
            best_path = [(-1, time, resources, can_build)] + p
        for robot_type in can_build:
            val = 0
            path = []
            if robot_type == 1 and b < blueprint[4][1]:
                val,path = calcMaxGeodesFixedOre(a,b+1,c, 
                        subResources(new_resources, blueprint, robot_type), 
                        blueprint, time - 1, fixed_ore)
            if robot_type == 2 and c < blueprint[4][2]:
                val,path = calcMaxGeodesFixedOre(a,b,c+1, 
                        subResources(new_resources, blueprint, robot_type),
                        blueprint, time - 1, fixed_ore)
            if robot_type == 3:
                v, path = calcMaxGeodesFixedOre(a,b,c, 
                        subResources(new_resources, blueprint, robot_type), 
                        blueprint, time - 1, fixed_ore)
                val = (time - 1) + v
            if val > best:
                best = val
                best_path = [(robot_type, time, resources)] + path
        return best, best_path

def partTest():
    exp_blues = [(4,2,(3,14),(2,7),(3,14,7)),(2,3,(3,8),(3,12),(3,8,12))]
    time1 = time.clock_gettime(time.CLOCK_MONOTONIC_RAW)
    best = 0
    best_path = []
    resources = (0,0,0)
    blue = exp_blues[0]
    for f in range(1, blue[4][0]+1):
        v,p = calcMaxGeodesFixedOre(1,0,0,resources, blue, 32, f)
        print(v,p,'\n')

    time2 = time.clock_gettime(time.CLOCK_MONOTONIC_RAW)
    print(time2 - time1, exp_blues[0], v)
    print(p)

def maxGeodesHeuristic(a, b, c, resources,blueprint,time):
    # making one geode robot every remaining turn
    #turns_per_grobot = blueprint[3][1]/c 
    return (time * (time - 1))//2

# build geode robot if can, otherwise obsidian robot, ignore other resources 
@lru_cache(maxsize=None)
def obsGeodesMax(c, obs, obs_cost, time):
    score = 0
    while(time > 0):
        if obs >= obs_cost:
            obs -= obs_cost
            score += time-1
            obs += c
        else:
            obs += c
            c += 1
        time -= 1
    return score
    

prune_dict = {}
@lru_cache(maxsize=None)
def calcMaxGeodesPruning(a,b,c,resources, blueprint, time, best_seen):
    if time <= 0:
        return 0,[]
    else:
        if best_seen >= obsGeodesMax(c,resources[2], blueprint[3][1], time):
            # doesn't matter, won't be used
            global prune_dict
            prune_dict[time] = prune_dict.get(time, 0) + 1
            #print("Pruned:",time, best_seen, prune_count)
            return 0,[]
        new_resources = tuple3Add(resources, (a,b,c))
        can_build = getRobotsCanBuild(blueprint, resources)
        if can_build == []:
            v, p = calcMaxGeodesPruning(a,b,c, new_resources, blueprint, time - 1, best_seen)
            return v, [(-1, time, resources, can_build)] + p
        best = -1
        best_path = []
        for robot_type in can_build:
            val = 0
            path = []
            sub_resources = subResources(new_resources, blueprint, robot_type)
            if robot_type == 3:
                val = (time - 1) 
                v, path = calcMaxGeodesPruning(a,b,c, sub_resources, blueprint, time - 1, best_seen - val)
                val += v
            if robot_type == 2 and c < blueprint[4][2]:
                val,path = calcMaxGeodesPruning(a,b,c+1, sub_resources, blueprint, time - 1, best_seen)
            if robot_type == 1 and b < blueprint[4][1]:
                val,path = calcMaxGeodesPruning(a,b+1,c, sub_resources, blueprint, time - 1, best_seen)
            if robot_type == 0 and a < blueprint[4][0]:
                val,path = calcMaxGeodesPruning(a+1,b,c, sub_resources, blueprint, time - 1, best_seen)
            if val > best:
                best = val
                #print(best)
                best_path = [(robot_type, time, resources)] + path
                if val > best_seen:
                    best_seen = val
            #        print(best_seen, time)
        no_op_best, no_op_path = calcMaxGeodesPruning(a,b,c, new_resources, blueprint, time - 1, best)
        if no_op_best > best:
            return no_op_best, [(-1, time, resources, can_build)] + no_op_path

        if best == -1:
            print("FUCKED UP AARON")
        return best, best_path

def part1():
    blues = []
    lines = getInput()
    lines = list(map(parseBlueprint, lines))
    for line in lines:
        # prices and then max prices to know when to stop building robots
        blues.append((line[1], line[2], (line[3], line[4]), (line[5], line[6]), 
            (max(line[2],line[3],line[5]), line[4], line[6])))

    print(blues)

    total = 0
    for i in range(len(blues)):
        blue = blues[i]
        mult = i + 1
        time1 = time.clock_gettime(time.CLOCK_MONOTONIC_RAW)
        v1,p1 = calcMaxGeodesPruning(1,0,0,(0,0,0), blue, 24, 0)
        time2 = time.clock_gettime(time.CLOCK_MONOTONIC_RAW)
        print(time2 - time1, i, blue, v1)
        #print(p1)
        #printPath(p1)
        total += v1 * mult
    print("Answer 1 =", total)

def part2():
    blues = []
    lines = getInput()
    lines = list(map(parseBlueprint, lines))
    for line in lines:
        # prices and then max prices to know when to stop building robots
        blues.append((line[1], line[2], (line[3], line[4]), (line[5], line[6]), 
            (max(line[2],line[3],line[5]), line[4], line[6])))

    exp_blues = [(4,2,(3,14),(2,7),(3,14,7)),(2,3,(3,8),(3,12),(3,8,12))]

    total = 0
    bests = []
    best_vals = []
    for blue in blues[:3]:
        time1 = time.clock_gettime(time.CLOCK_MONOTONIC_RAW)
        v,p = calcMaxGeodesPruning(1,0,0,(0,0,0), blue, 32, 0)
        time2 = time.clock_gettime(time.CLOCK_MONOTONIC_RAW)
        print(time2 - time1, blue, v)
        print(v, '\n')
        bests.append((v,p))
        best_vals.append(v)
    total = 1
    for b in best_vals:
        total *= b
        print(b)

    print("Answer 2 =", total)
part2()
print(prune_dict)
