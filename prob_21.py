import re
def getInput():
    with open('inputs/input_21.txt', 'r') as f:
        lines = f.read().splitlines()
        return lines

def parseLine(line):
    pipesre = '[a-z]{4}'
    numre = '[0-9]+'
    
    names = re.findall(pipesre, line)

    if len(names) != 3:
        numre = '[0-9]+'
        number = re.search(numre, line)
        return (True, [names[0], number[0]])

    puncre = '[+\-*/]'
    punc = re.search(puncre, line)

    return (False, [names[0], names[1], punc[0], names[2]]) 

def doMath(a, punc, b):
    if punc == "/":
        return a / b
    elif punc == "+":
        return a + b
    elif punc == "*":
        return a * b
    elif punc == "-":
        return a - b

def callMonkey(call, to_call):
    name1 = to_call[0]
    name2 = to_call[1]
    name3 = to_call[3]
    punc = to_call[2]
    if name2 in call and name3 in call:
        return True, doMath(call[name2], punc, call[name3]), name1
    return False, 0, name1

def solveForName(monkey, given_val, uncalled, called, name_to_solve):
    name2 = uncalled[monkey][0]
    punc = uncalled[monkey][1]
    name3 = uncalled[monkey][2]
    if name3 == name_to_solve:
        if name2 not in called:
            print("key error: ", name2, "not in called :(")
            return
        val2 = called[name2]
        if punc == "/":
            return val2 / given_val 
        elif punc == "+":
            return given_val - val2
        elif punc == "*":
            return given_val / val2
        elif punc == "-":
            return val2 - given_val
    if name2 == name_to_solve:
        if name3 not in called:
            print("key error: ", name3, "not in called :(")
            return
        val3 = called[name3]
        if punc == "/":
            return given_val * val3
        elif punc == "+":
            return given_val - val3
        elif punc == "*":
            return given_val / val3
        elif punc == "-":
            return given_val + val3
    else:
        print(monkey, uncalled[monkey], name_to_solve)


def part1():
    with open('inputs/input_21.txt', 'r') as f:
         lines = f.read().splitlines()

    root = 'root'
    call = {}
    uncalled = {}
    for l in lines:
        k = parseLine(l)
        if k[0]:
            name = k[1][0]
            number = int(k[1][1])
            call[name] = number
            #print(name, number)
        else:
            name1 = k[1][0]
            name2 = k[1][1]
            name3 = k[1][3]
            punc = k[1][2]
            uncalled[name1] = (name2, punc, name3)

    seen = {}
    #print(call)
    index = 0
    stack = [root]
    while (stack != []):
        #print(len(stack))
        monkey = stack.pop()
        if monkey in call:
            #print(monkey, uncalled[monkey], call[monkey])
            continue
        name2 = uncalled[monkey][0]
        punc = uncalled[monkey][1]
        name3 = uncalled[monkey][2]
        if name3 in stack or name2 in stack:
            print("RECURSION")
            print(uncalled[monkey])
        if name2 not in call:
            if name2 in stack:
                break
            stack.append(monkey)
            stack.append(name2)
            if name3 not in call:
                stack.append(name3)
            continue
        if name3 not in call:
            stack.append(monkey)
            stack.append(name3)
            continue
        call[monkey] = doMath(call[name2], punc, call[name3])
    
    if root in call:
        print("Answer 1 = ", int(call[root]))



def part2():
    with open('inputs/input_21.txt', 'r') as f:
         lines = f.read().splitlines()

    root = 'root'
    humn = 'humn'

    call = {}
    uncalled = {}
    for l in lines:
        k = parseLine(l)
        if k[0]:
            name = k[1][0]
            number = int(k[1][1])
            call[name] = number
            #print(name, number)
        else:
            name1 = k[1][0]
            name2 = k[1][1]
            name3 = k[1][3]
            punc = k[1][2]
            uncalled[name1] = (name2, punc, name3)



    call[humn] = 0
    seen = {}
    #print(call)
    index = 0
    stack = [root]
    toFind = []
    while (stack != []):
        #print(len(stack))
        monkey = stack.pop()
        if monkey in call:
            #print(monkey, uncalled[monkey], call[monkey])
            continue
        name2 = uncalled[monkey][0]
        punc = uncalled[monkey][1]
        name3 = uncalled[monkey][2]
        if name2 == humn:
            toFind = stack.copy()
            toFind.append(monkey)
            toFind.append(name2)

        if name3 == humn:
            toFind = stack.copy()
            toFind.append(monkey)
            toFind.append(name3)
        if name3 in stack or name2 in stack:
            print("RECURSION")
            print(uncalled[monkey])
        if name2 not in call:
            if name2 in stack:
                break
            stack.append(monkey)
            stack.append(name2)
            continue
        if name3 not in call:
            stack.append(monkey)
            stack.append(name3)
            continue
        call[monkey] = doMath(call[name2], punc, call[name3])
    
    '''
    print(call[humn])
    print(toFind)
    print(uncalled['qmfl'])
    print(call['qdpj'])
    print(call['bbwc'])
    print("Solved:", solveForName('qmfl', call['qdpj'], uncalled, call, 'mflw'))
    '''

    given_val = call['qdpj']
    for x in range(len(toFind) - 2):
        given_name = toFind[x+1]
        solve_for = toFind[x+2]
        val = solveForName(given_name, given_val, uncalled, call, solve_for)
        given_val = val
        call[solve_for] = val

    if humn in call:
        print("Answer 2 = ", int(call[humn]))

        

part1()
part2()

