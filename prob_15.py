import re
exp = '''\
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
'''

def parseLine(line):
    numre = '[0-9]+'
    items = list(map(int, re.findall(numre, line)))
    return items

def getInput():
    with open('inputs/input_15.txt', 'r') as f:
        return list(map(parseLine, f.read().splitlines()))

def getExp():
    return list(map(parseLine, exp.splitlines()))

def getRanges(x,y, txd, yline):
    ydist = abs(y-yline) 
    xdist = txd - ydist 
    if xdist < 0:
        return []
    return [(x-xdist, x+xdist)]

def part1():
    lines = getInput()
    offranges = []
    fixed_line = 2000000
    beacon_set = set()
    for line in lines:
        txd = abs(line[2]-line[0]) + abs(line[3]-line[1])
        beacon_set.add((line[2],line[3]))
        xr = getRanges(line[0],line[1], txd, fixed_line)
        offranges += xr
    offranges.sort(key=lambda x: x[0])
    newoffs = []
    i = 0
    #print(offranges)
    while i < len(offranges) - 1:
        ofa = offranges[i]
        ofb = offranges[i+1]
        if ofa[1] >= ofb[0]:
            newrange = (ofa[0], max(ofa[1], ofb[1]))
            offranges = [newrange] + offranges[2:]
            #print(offranges)
            continue
        else:
            i += 1

    total = 0
    for x in offranges:
        # +1 because range is inclusive
        total += x[1] - x[0] + 1
    for y in list(beacon_set):
        if y[1] == fixed_line:
            total -= 1
    print("Answer 1 =", total)

def checkAllDistances(sensors, location):
    x = location[0]
    y = location[1]
    for sensor in sensors:
        txd = abs(x - sensor[0]) + abs(y - sensor[1])
        if txd <= sensor[2]:
            return False
    return True

def crossSensors(sensors):
    results = []
    for s1 in sensors:
        x1,y1,txd1,_ = s1
        for s2 in sensors:
            if s1[0] <= s2[0] and s1 != s2:
                x2,y2,txd2,_ = s2
                if abs(abs(x1-x2) + abs(y1-y2) - (txd1 + txd2)) == 2:
                    results += [(s1,s2)]
    return results

def combineRanges(ranges):
    i = 0
    ranges.sort(key = lambda x:x[0])
    while i < len(ranges) - 1:
        ofa = ranges[i]
        ofb = ranges[i+1]
        if ofa[1] >= ofb[0]:
            newrange = (ofa[0], max(ofa[1], ofb[1]))
            ranges = ranges[:i] + [newrange] + ranges[i+2:]
            continue
        else:
            i += 1
    #if len(ranges) > 1:
        #print(ranges)
    return ranges

def buildRanges(sensors, yline): 
    ranges = []
    for sensor in sensors:
        x = sensor[0]
        y = sensor[1]
        txd = sensor[2]
        ydist = abs(y-yline) 
        xdist = txd - ydist 
        if xdist >= 0:
            ranges.append((x-xdist, x+xdist))
    return ranges

def checkLine(sensors, yline):
    ranges = combineRanges(buildRanges(sensors, yline))
    if len(ranges) == 0:
        print("What's up with that? 0 length range")
        return False
    if len(ranges) == 1:
        r = ranges[0]
        if r[0] <= 0 and r[1] >= 2000000:
            return False
        #print("it was only one long?", r)
        return True
    else:
        #print("We did it!!!", yline, ranges)
        return True

def getFirstFreeIntFromRanges(ranges):
    if len(ranges) == 0:
        return -1
    else:
        i = 0
        while i < len(ranges) - 1:
            if ranges[i][1] + 1 < ranges[i+1][0]:
                return ranges[i][1] + 1
            i += 1
        return -1
            
def part2():
    lines = getInput()
    offranges = []
    fixed_line = 2000000
    beacon_set = set()
    sensors = []
    for line in lines:
        txd = abs(line[2]-line[0]) + abs(line[3]-line[1])
        sensors.append((line[0], line[1], txd, (line[2],line[3])))

    answer = 0
    print("might take a minute")
    for y in range(0,4000000):
        b = checkLine(sensors, y)
        if b:
            answer = y
            print("Found it!")
            break

    ranges = combineRanges(buildRanges(sensors, answer))
    x = getFirstFreeIntFromRanges(ranges)
    #print(x,y)
    print("Answer 2 =", x * 4000000 + y)

part1()
part2()
