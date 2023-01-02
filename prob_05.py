with open('inputs/input_05.txt','r') as f:
    x = f.read().splitlines()

start = x[:8]
moves = x[10:]

def parseBoxes(start):
    boxes = {}
    start = start[::-1]
    for l in start:
        z = 0
        while(4 * z + 1 < len(l)):
            index = z * 4 + 1
            if (z not in boxes):
                boxes[z] = [l[index]]
            elif (l[index] != " "):
                boxes[z] = boxes[z] + [l[index]]
            z += 1
    return boxes


def parseMove(line):
    x = line.split()
    return (int(x[1]),int(x[3]),int(x[5]))

def move(boxes, number, start, end):
    start = start-1
    end = end-1
    move = boxes[start][-number:]
    boxes[start] = boxes[start][0:-number]
    boxes[end] = boxes[end] + move[::-1]
    return boxes

def moveV2(boxes, number, start, end):
    start = start-1
    end = end-1
    move = boxes[start][-number:]
    boxes[start] = boxes[start][0:-number]
    boxes[end] = boxes[end] + move
    return boxes

def moveByLine(boxes, line):
    (number, start, end) = parseMove(line)
    return move(boxes, number, start, end)

def moveByLineV2(boxes, line):
    (number, start, end) = parseMove(line)
    return moveV2(boxes, number, start, end)

boxes = parseBoxes(start)
for l in moves:
    boxes = moveByLine(boxes, l)

answer = ""
for x in range(0,9):
    answer += boxes[x][-1]
print("Answer 1 =", answer)

boxes2 = parseBoxes(start)
for l in moves:
    boxes2 = moveByLineV2(boxes2, l)

answer = ""
for x in range(0,9):
    answer += boxes2[x][-1]
print("Answer 2 =", answer)

