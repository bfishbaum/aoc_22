import re
import time

from functools import lru_cache

import itertools
example = '''\
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
'''

with open('inputs/input_16.txt','r') as f:
    lines = f.read().splitlines()

#lines = example.splitlines()

def parseLine(line):
    pipesre = '[A-Z]{2}'
    outs = re.findall(pipesre, line)

    ratere = '[0-9]+'
    rate = re.findall(ratere, line)
    return outs[0], outs[1:], int(rate[0])

def buildNetwork(lines):
    pipes = {}
    for line in lines:
        loc, nexts, rate = parseLine(line)
        pipes[loc] = (rate, nexts)
    return pipes

pipes = buildNetwork(lines)
#print(pipes)

real_pipes = []
for p in pipes.keys():
    if pipes[p][0] != 0:
        real_pipes.append(p)
print(real_pipes)

def buildDistanceTree(pipes, root, real):
    result = {}
    frontier = [root]
    seen = set()
    realset = set(real)
    count = 0
    while frontier != []:
        new_front = []
        for f in frontier:
            if f in seen:
                continue
            else:
                seen.add(f)
                if f in realset and f != root:
                    result[f] = count
                new_front.append(f)
            nexts = pipes[f][1]
            new_front += nexts
        count += 1
        frontier = new_front
    return result

def buildRealNetwork(pipes, real):
    result = {}
    for x in real:
        result[x] = buildDistanceTree(pipes, x, real)
    return result

tree = buildRealNetwork(pipes, real_pipes)
tree["AA"] = buildDistanceTree(pipes, "AA", real_pipes)
print(tree)

scores = {f:pipes[f][0] for f in real_pipes}

optimize = False
#optimize = True
total_time = 26

def bal(dloc, eloc, etime, time, seen):
    global tree
    global optimize
    nexts = list(filter(lambda x: x not in seen, real_pipes))
    dadj = []
    #yes_print = ("CX" in nexts and "QC" in nexts and dloc == "EA" and time == 8)
    yes_print = False
    if yes_print:
        print("HERE ", dloc, eloc, etime, time, seen, nexts)
    for r1 in nexts:
        if r1 == eloc and tree[dloc][r1] > etime:
            if yes_print:
                print('Seen: ', r1)
            continue
        if tree[dloc][r1] >= time:
            if yes_print:
                print('Toolate: ', r1)
            continue
        toolow = False
        if optimize and time > 10:
            for n in nexts:
                if (scores[n] >= scores[r1] and tree[dloc][n] <= tree[dloc][r1] and 
                        (scores[n] > scores[r1] or tree[dloc][n] < tree[dloc][r1])):
                    toolow = True
                    break
        if toolow:
            if yes_print:
                print(r1, "toolow compared to", n)
            continue
        dadj.append((r1, tree[dloc][r1]))
    if yes_print:
        print("END: ", dadj, "\n\n")
    return dadj

# build adjacency power set
def baps(dloc, eloc, time, seen):
    global optimize
    global tree
    nexts = list(filter(lambda x: x not in seen, real_pipes))
    result = []
    dadj = []
    for r1 in real_pipes:
        if r1 in seen:
            continue
        if tree[dloc][r1] >= time:
            continue
        toolow = False
        if optimize:
            for n in nexts:
                if (scores[n] >= scores[r1] and tree[dloc][n] <= tree[dloc][r1] and 
                        (scores[n] > scores[r1] or tree[dloc][n] < tree[dloc][r1])):
                    toolow = True
                    break
        if toolow:
            continue
        dadj.append((r1, tree[dloc][r1]))
    if dadj == []:
        # dummy answer so cross product isn't empty
        dadj.append(("AA", 100))
    eadj = []
    for r2 in real_pipes:
        if r2 in seen:
            continue
        if tree[eloc][r2] >= time:
            continue
        toolow = False
        if optimize:
            for n in nexts:
                if (scores[n] >= scores[r2] and tree[eloc][n] <= tree[eloc][r2] and 
                        (scores[n] > scores[r2] or tree[eloc][n] < tree[eloc][r2])):
                    toolow = True
                    break
        if toolow:
            continue
        eadj.append((r2, tree[eloc][r2]))
    if eadj == []:
        # dummy answer so cross product isn't empty
        eadj.append(("AA", 100))

    result = itertools.product(dadj, eadj)
    result = list(filter(lambda x: x[0][0] != x[1][0], result))
    if eloc == dloc:
        # remove half if they are the same
        result = list(filter(lambda x: x[0][0] > x[1][0], result))
    return result

#@lru_cache(maxsize=None)
def mfrn(dloc, dtime, eloc, etime, time, seen):
    #print(dloc, dtime, eloc, etime, time, seen)
    if (time == 0 or time == 1):
        return 0, ([],[])
    global scores
    global tree
    global total_time
    global optimize

    d_traveling = dtime > 0
    e_traveling = etime > 0

    if d_traveling and e_traveling:
        time_jump = min(dtime, etime)
        v, b = mfrn(dloc, dtime-time_jump, eloc, etime-time_jump, time - time_jump, seen)
        return v,b
    elif not d_traveling and not e_traveling:
        value = 0
        don = 1
        eon = 1
        if dloc not in seen:
            seen.add(dloc)
            value += (time - 1) * scores[dloc]
            don = 0
        if eloc not in seen:
            seen.add(eloc)
            value += (time - 1) * scores[eloc]
            eon = 0
        adjs = baps(dloc, eloc, time, seen)
        if adjs == []:
            dpath = []
            epath = []
            if don == 0:
                seen.remove(dloc)
                dpath.append((dloc, dtime))
            if eon == 0:
                seen.remove(eloc)
                epath.append((eloc, etime))
            return value,(dpath,epath)
        best = 0
        best_path = ([],[])
        count = 0
        for x in adjs:
            v, path = mfrn(x[0][0], x[0][1]-don, x[1][0], x[1][1]-eon, time-1, seen)
            if time == total_time:
                count += 1
                print(count, len(adjs), v, path)
            if v > best:
                best = v
                best_path = path
        if don == 0:
            seen.remove(dloc)
        if eon == 0:
            seen.remove(eloc)
        #if time > 17:
            #print ("Done loop: ", time, dloc, eloc)
        #    print(time, eloc, dloc, seen, b)

        return best + value, ([(dloc, time)] + best_path[0], [(eloc, time)] + best_path[1])
    elif not d_traveling and e_traveling:
        value = 0
        don = 1
        if dloc not in seen:
            seen.add(dloc)
            value += (time - 1) * scores[dloc]
            don = 0
        adjs = bal(dloc, eloc, etime, time, seen)
        if adjs == []:
            if don == 0:
                seen.remove(dloc)
            return value, ([], [])
        best = 0
        best_path = ([],[])
        for adj in adjs:
            v, path = mfrn(adj[0], adj[1] - don, eloc, etime - 1, time - 1, seen)
            if v > best:
                best = v
                best_path = path
        if don == 0:
            seen.remove(dloc)
        return value + best, ([((dloc + "_D", adjs), time)] + best_path[0], best_path[1])
    elif d_traveling and not e_traveling:
        v, (dp, ep) = mfrn(eloc, etime, dloc, dtime, time, seen)
        return v, (ep, dp)
    else:
        print("Shouldn't be here! ", eloc, etime, dloc, dtime, time) 
        return 0,([],[])



seen = set()
seen.add("AA")

print(scores)
print(tree.keys())

time_start = time.clock_gettime(time.CLOCK_MONOTONIC_RAW)

v, b = mfrn("AA", 0, "AA", 0, total_time, seen)
time_end = time.clock_gettime(time.CLOCK_MONOTONIC_RAW)
print(v)
print(b)
print("Total time = ", time_end - time_start)



memoize = {}
def maximizeFlow(pipes, location, time, enabled, previous):
    global memoize
    if (location, time, tuple(enabled)) in memoize:
        return memoize[(location, time, tuple(enabled))]
    if (time <= 1):
        memoize[(location, time, tuple(enabled))] = 0
        return 0
    (rate, nexts) = pipes[location]
    if rate == 0 or location in enabled:
        max_flow = 0
        for nxt in nexts:
            if nxt in previous:
                continue
            flow = maximizeFlow(pipes, nxt, time - 1, enabled, previous + [location])
            if flow > max_flow:
                max_flow = flow
        memoize[(location, time, tuple(enabled))] = max_flow
        return max_flow
    # not enabled AND rate != 0
    else:
        # turned on
        turn_on_flow = (time-1) * rate
        max_flow = 0
        for nxt in nexts:
            flow = maximizeFlow(pipes, nxt, time - 2, enabled+[location], [location])
            if flow > max_flow:
                max_flow = flow
        turn_on_flow += max_flow

        max_flow = 0
        for nxt in nexts:
            flow = maximizeFlow(pipes, nxt, time - 1, enabled, previous)
            if flow > max_flow:
                max_flow = flow
        memoize[(location, time, tuple(enabled))] = max(turn_on_flow, max_flow)
        return max(turn_on_flow, max_flow)

memoize2 = {}
def maximizeFlowV2(pipes, loc, loc2, time, enabled, visited):
    if (time <= 1):
        return 0
    if (time >= 18):
        print(time, enabled)
    global memoize
    if len(enabled) == 15:
        return 0
    if (loc, loc2, time, tuple(enabled)) in memoize2:
        return memoize2[(loc, loc2, time, tuple(enabled))]


    (rate, nexts) = pipes[loc]
    (rate2, nexts2) = pipes[loc2]
    v = visited.copy()
    # both valves are useless move on
    if ((rate == 0 or loc in enabled) and (rate2 == 0 or loc2 in enabled)):
        max_flow = 0
        for nxt in nexts:
            if nxt in visited:
                continue
            for nxt2 in nexts2: 
                if nxt2 in visited:
                    continue
                v.add(loc)
                v.add(loc2)
                flow = maximizeFlowV2(pipes, nxt, nxt2, time - 1, enabled, v)
                if flow > max_flow:
                    max_flow = flow
        memoize2[(loc, loc2, time, tuple(enabled))] = max_flow
        memoize2[(loc2, loc, time, tuple(enabled))] = max_flow
        return max_flow
    # both valves can be turned on
    elif (rate != 0 and loc not in enabled) and (rate2 != 0 and loc2 not in enabled) and loc != loc2:
        both_on_flow = (time-1) * (rate + rate2) + maximizeFlowV2(pipes, loc, loc2, time - 1, enabled+[loc,loc2], v)

        one_on_flow = (time-1) * rate
        max_flow = 0
        for nxt2 in nexts2:
            if nxt2 in visited:
                continue
            v.add(loc2)
            flow = maximizeFlowV2(pipes, loc, nxt2, time - 1, enabled + [loc], v)
            if flow > max_flow:
                max_flow = flow
        one_on_flow += max_flow

        two_on_flow = (time-1) * rate2
        max_flow = 0
        for nxt in nexts:
            if nxt in visited:
                continue
            v.add(loc)
            flow = maximizeFlowV2(pipes, nxt, loc2, time - 1, enabled + [loc2], v)
            if flow > max_flow:
                max_flow = flow
        two_on_flow += max_flow

        none_on_flow = 0
        max_flow = 0
        for nxt in nexts:
            if nxt in visited:
                continue
            for nxt2 in nexts2: 
                if nxt2 in visited:
                    continue
                v.add(loc)
                v.add(loc2)
                flow = maximizeFlowV2(pipes, nxt, nxt2, time - 1, enabled, v)
                if flow > max_flow:
                    max_flow = flow
        none_on_flow += max_flow

        high_flow = max(both_on_flow, one_on_flow, two_on_flow, none_on_flow)

        memoize2[(loc, loc2, time, tuple(enabled))] = high_flow
        memoize2[(loc2, loc, time, tuple(enabled))] = high_flow
        return high_flow


    # not enabled AND rate != 0
    elif (rate != 0 and loc not in enabled):
        # turned on
        turn_on_flow = (time-1) * rate
        max_flow = 0
        for nxt2 in nexts2:
            if nxt2 in visited:
                continue
            v.add(loc2)
            flow = maximizeFlowV2(pipes, loc, nxt2, time - 1, enabled+[loc], v)
            if flow > max_flow:
                max_flow = flow
        turn_on_flow += max_flow

        # not turned on
        turn_off_flow = 0
        max_flow = 0
        for nxt in nexts:
            if nxt in visited:
                continue
            for nxt2 in nexts2: 
                if nxt2 in visited:
                    continue
                v.add(loc)
                v.add(loc2)
                flow = maximizeFlowV2(pipes, nxt, nxt2, time - 1, enabled, v)
                if flow > max_flow:
                    max_flow = flow

        turn_off_flow += max_flow

        high_flow = max(turn_on_flow, turn_off_flow)
        memoize2[(loc, loc2, time, tuple(enabled))] = high_flow
        memoize2[(loc2, loc, time, tuple(enabled))] = high_flow
        return high_flow

    elif (rate2 != 0 and loc2 not in enabled):
        # turned on
        turn_on_flow = (time-1) * rate2
        max_flow = 0
        for nxt in nexts:
            if nxt in visited:
                continue
            v.add(loc)
            flow = maximizeFlowV2(pipes, nxt, loc2, time - 1, enabled+[loc2], v)
            if flow > max_flow:
                max_flow = flow
        turn_on_flow += max_flow

        # not turned on
        turn_off_flow = 0
        max_flow = 0
        for nxt in nexts:
            if nxt in visited:
                continue
            for nxt2 in nexts2: 
                if nxt2 in visited:
                    continue
                v.add(loc)
                v.add(loc2)
                flow = maximizeFlowV2(pipes, nxt, nxt2, time - 1, enabled, v)
                if flow > max_flow:
                    max_flow = flow
        turn_off_flow += max_flow

        high_flow = max(turn_on_flow, turn_off_flow)
        memoize2[(loc, loc2, time, tuple(enabled))] = high_flow
        memoize2[(loc2, loc, time, tuple(enabled))] = high_flow
        return high_flow
    return 0

#print(maximizeFlow(pipes, "AA", 30, [], []))
#print(maximizeFlowV2(pipes, "AA", "AA", 26, [], set()))
