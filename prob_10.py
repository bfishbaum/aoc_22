def getInput():
    with open('inputs/input_10.txt','r') as f:
        lines = f.read().splitlines()
        return lines 

def part1():
    lines = getInput()
    cycle = 0
    value = 1
    total = 0
    for line in lines:
        if line[0] == "n":
            cycle += 1
            if (cycle % 40 == 20 and cycle < 221):
                total += value * cycle
            #print("noop")
        elif line[0] == "a":
            cycle += 1
            if (cycle % 40 == 20 and cycle < 221):
                total += value * cycle
            cycle += 1
            if (cycle % 40 == 20 and cycle < 221):
                total += value * cycle
            val = int(line[5:])
            value += val

    print("Answer 1 =", total)

part1()

def printScreen(screen):
    for l in range(0,len(screen),40):
        print(''.join(screen[l:l+40]))

#screen = ["#" for x in range(240)]

def part2():
    cycle = 0
    value = 1
    screen = []
    lines = getInput()
    for line in lines:
        #print(cycle, value, line)
        if line[0] == "n":
            if (abs(value-(cycle % 40)) <= 1):
                screen.append("##")
            else:
                screen.append("..")
            cycle += 1
            #print("noop")
        elif line[0] == "a":
            if (abs(value-(cycle % 40)) <= 1):
                screen.append("##")
            else:
                screen.append("..")
            cycle += 1

            if (abs(value-(cycle % 40)) <= 1):
                screen.append("##")
            else:
                screen.append("..")
            cycle += 1
            val = int(line[5:])
            value += val

    print("Answer 2 = [READ BELOW] (should be BGKAEREZ)")
    printScreen(screen)

part2()
        
