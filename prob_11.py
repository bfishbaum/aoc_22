import re
def getInput():
    with open('inputs/input_11.txt', 'r') as f:
        return f.read().split('\n\n')

def parseMonkey(monkey):
    ml = monkey.splitlines()

    numre = '[0-9]+'
    items = list(map(int, re.findall(numre, ml[1])))
    div_test = int(re.search(numre, ml[3])[0])
    to_true = int(re.search(numre, ml[4])[0])
    to_false = int(re.search(numre, ml[5])[0])

    return items, div_test, to_true, to_false

def getMonkeyOps():
    return [
            lambda x: x*11,
            lambda x: x+1,
            lambda x: x*x,
            lambda x: x+2,
            lambda x: x+6,
            lambda x: x+7,
            lambda x: x*7,
            lambda x: x+8]

def appendItem(monkeys, to_monkey, worry):
    monkeys[to_monkey] = (monkeys[to_monkey][0] + [worry],
            monkeys[to_monkey][1],
            monkeys[to_monkey][2],
            monkeys[to_monkey][3],
            monkeys[to_monkey][4],
            monkeys[to_monkey][5])

def simulateTurn(monkeys, turn):
    monkey = monkeys[turn]
    items = monkey[0]
    op = monkey[4]
    div_test = monkey[1]
    to_true, to_false = monkey[2],monkey[3]
    count = 0
    for item in items:
        worry = op(item)
        worry //= 3
        if worry % div_test == 0:
            appendItem(monkeys, to_true, worry)
        else:
            appendItem(monkeys, to_false, worry)
        count += 1
    monkeys[turn] = ([], div_test, to_true, to_false, op, monkey[5] + count)


def simulateRound(monkeys, number):
    for x in range(number):
        simulateTurn(monkeys, x)

def part1():
    monkeys_text = getInput()
    monkeys = {}
    monkey_ops = getMonkeyOps()
    for i in range(len(monkeys_text)):
        items, div_test, to_true, to_false = parseMonkey(monkeys_text[i])
        monkeys[i] = (items, div_test, to_true, to_false, monkey_ops[i], 0)
    #print(monkeys)
    for x in range(20):
        #print(x)
        simulateRound(monkeys, 8)
    #print(monkeys)
    totals = []
    for k in monkeys.keys():
        totals.append(monkeys[k][5])
    totals = sorted(totals) 
    print("Answer 1 =", totals[-1] * totals[-2])


def simulateTurnPart2(monkeys, turn, div):
    monkey = monkeys[turn]
    items = monkey[0]
    op = monkey[4]
    div_test = monkey[1]
    to_true, to_false = monkey[2],monkey[3]
    count = 0
    for item in items:
        worry = op(item)
        worry = worry % div
        if worry % div_test == 0:
            appendItem(monkeys, to_true, worry)
        else:
            appendItem(monkeys, to_false, worry)
        count += 1
    monkeys[turn] = ([], div_test, to_true, to_false, op, monkey[5] + count)

def simulateRoundPart2(monkeys, number, div):
    for x in range(number):
        simulateTurnPart2(monkeys, x, div)

def part2():
    monkeys_text = getInput()
    monkeys = {}
    monkey_ops = getMonkeyOps()
    for i in range(len(monkeys_text)):
        items, div_test, to_true, to_false = parseMonkey(monkeys_text[i])
        monkeys[i] = (items, div_test, to_true, to_false, monkey_ops[i], 0)
    #####
    ##### MODULO DIV RETAINS ALL DIVISIBILITY PROPERTYS
    #####
    div = 1
    for k in monkeys.keys():
        div *= monkeys[k][1]
    #print(div)
    for x in range(10000):
        #print(x)
        simulateRoundPart2(monkeys, 8, div)
    #print(monkeys[0][0])
    totals = []
    for k in monkeys.keys():
        totals.append(monkeys[k][5])
    totals = sorted(totals) 
    print("Answer 2 =",totals[-1] * totals[-2])

part1()
part2()
