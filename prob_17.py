import sys
import time
def getInput():
    with open('inputs/input_17.txt', 'r') as f:
        line = f.read().strip()
        return line

def add(t1,t2):
    return (t1[0] + t2[0], t1[1] + t2[1])

verbose = 0
frame_rate = 10

pieces = [[(0,0),(1,0),(2,0),(3,0)], # - shape
          [(0,1),(1,0),(1,1),(1,2),(2,1)], # + shape
          [(0,0),(1,0),(2,0),(2,1),(2,2)], # backwards L shape
          [(0,0),(0,1),(0,2),(0,3)], # | shpae
          [(0,0),(0,1),(1,0),(1,1)]] # square shape

COLORS = ['\033[95m',
            '\033[94m',
            '\033[96m',
            '\033[92m',
            '\033[91m',
            '\033[93m',
            '\033[99m']

def printCaveWithFalling(rocks, highest_rock, location, piece):
    new_pieces = list(map(lambda x: add(x,location), piece))
    cave = ""
    bottom = 35 * "_"
    for y in range(location[1] + 10 ,max(location[1]-10,-1),-1):
        for loop in range(3):
            cave += "|"
            for x in range(7):
                if (x,y) in new_pieces:
                    cave += COLORS[6]
                    cave += "@@@@"
                    cave += COLORS[5]
                    cave += "|"
                elif (x,y) in rocks:
                    #cave += colors[(x,y)]
                    cave += "####"
                    #cave += COLORS[5]
                    cave += "|"
                else:
                    cave += "....|"
            if loop == 2:
                cave += "|  " + str(y) + "\n"
            else:
                cave += "|\n"

    cave += "+" + bottom + "+"
    print(cave)

def printCave(rocks, highest_rock, colors):
    cave = ""
    bottom = 35 * "_"
    for y in range(highest_rock,-1,-1):
        for loop in range(3):
            cave += "|"
            for x in range(7):
                if (x,y) in rocks:
                    cave += colors[(x,y)]
                    cave += "####"
                    cave += COLORS[5]
                    cave += "|"
                else:
                    cave += "....|"
            if loop == 2:
                cave += "|  " + str(y) + "\n"
            else:
                cave += "|\n"

    cave += "+" + bottom + "+"
    print(cave)


def didCollide(piece, location, rocks):
    for point in piece: 
        np = add(point, location)
        if np[0] < 0 or np[0] >= 7 or np[1] < 0 or np in rocks:
            return True
    return False

def insertPiece(piece, rocks, highest_rock, jets, jets_index):
    global verbose
    global frame_rate
    location = (2, highest_rock + 4)
    while(True):
        #print(jets_index)
        if verbose == 2:
            printCaveWithFalling(rocks, highest_rock + 6, location, piece)
            time.sleep(1/frame_rate)

        if jets[jets_index] == "<":
            new_loc = add(location, (-1,0))
        elif jets[jets_index] == ">": 
            new_loc = add(location, (1,0))
        else:
            return
        if not didCollide(piece, new_loc, rocks):
            location = new_loc
        else:
        jets_index = (jets_index + 1) % len(jets)
        if verbose == 2:
            printCaveWithFalling(rocks, highest_rock + 6, location, piece)
            time.sleep(1/frame_rate)

        down_loc = add(location, (0,-1))
        if not didCollide(piece, down_loc, rocks):
            location = down_loc 
            #print("Down", down_loc)
        else:
            if verbose == 2:
                printCaveWithFalling(rocks, highest_rock + 6, location, piece)
                time.sleep(1/frame_rate)
            #print("Done", location)
            return location, jets_index


def part1():
    global verbose
    verbose = 0
    global frame_rate
    frame_rate = 1
    jets = getInput()

    #print(len(jets))
    #jets = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"
    jets_index = 0
    rocks = set()
    highest_rock = -1
    colors = {}
    count = 0
    for i in range(2022):
        piece = pieces[i % 5]
        location, jets_index = insertPiece(piece, rocks, highest_rock, jets, jets_index)
        count += 1
        for pt in piece:
            rocks.add(add(location, pt))
            colors[add(location, pt)] = COLORS[i % 5]
            highest_rock = max(list(rocks), key = lambda x: x[1])[1]
        #printCave(rocks, highest_rock, colors)
        #print("\n")
    #printCave(rocks, highest_rock, colors)
    print("Answer 1 = ",highest_rock + 1)

def part2():
    global verbose
    verbose = 0
    global frame_rate
    frame_rate = 1
    jets = getInput()

    #print(len(jets))
    #jets = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"
    jets_index = 0
    rocks = set()
    highest_rock = -1
    colors = {}
    count = 0
    repeats = {}
    i = 0
    top = 10**12
    imag_height = 0
    looped = False
    while i < top:
        if i % 1000 == 0:
            print(i)
        piece = pieces[i % 5]
        location, jets_index = insertPiece(piece, rocks, highest_rock, jets, jets_index)
        # if we see this we can count the height distance change in steps
        repre = (location[0], jets_index, i%5)
        for pt in piece:
            rocks.add(add(location, pt))
            colors[add(location, pt)] = COLORS[i % 5]
            highest_rock = max(list(rocks), key = lambda x: x[1])[1]
        if (not looped):
            if (repre in repeats):
                #looped = True
                l = repeats[repre]
                if len(l) == 3:
                    dh1, di1 = l[1][0] - l[0][0], l[1][1]-l[0][1]
                    dh2, di2 = l[2][0] - l[1][0], l[2][1]-l[1][1]
                    if dh1 == dh2 and di1 == di2:
                        diff_high, diff_i = dh1, di1
                        loops = ((top - i) // diff_i)
                        after_loops_i = i + loops * diff_i
                        imag_height = loops * diff_high
                        looped = True
                        i = after_loops_i
                        i += 1
                        continue
                repeats[repre] = repeats[repre] + [(highest_rock,i)]
            else:
                repeats[repre] = [(highest_rock,i)]
        #printCave(rocks, highest_rock, colors)
        #print("\n")
        i += 1
    print("Answer 2 =", highest_rock + imag_height+1)

part1()
part2()

