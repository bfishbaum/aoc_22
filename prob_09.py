with open('inputs/input_09.txt','r') as f:
    x = f.read().splitlines()

def sign(x):
    if x < 0:
        return -1
    elif x == 0:
        return 0
    return 1

def updateHead(head, direction):
    if direction == "U":
        return (head[0], head[1] + 1)
    elif direction == "D":
        return (head[0], head[1] - 1)
    elif direction == "R":
        return (head[0] + 1, head[1])
    elif direction == "L":
        return (head[0] - 1, head[1])

def updateTail(tail, head):
    diff = (head[0] - tail[0], head[1] - tail[1])
    if abs(diff[0]) > 1 or abs(diff[1]) > 1:
        return (tail[0] + sign(diff[0]), tail[1] + sign(diff[1]))
    return tail

def updateTails(tails, head):
    new_tails = []
    for t in tails:
        new_loc = updateTail(t, head)
        head = new_loc
        new_tails.append(new_loc)
    return new_tails

points = set()
points.add((0,0))
head = (0,0)
tail = (0,0)
for line in x:
    direction = line[0]
    distance = int(line[1:])
    for i in range(distance):
        head = updateHead(head, direction)
        tail = updateTail(tail, head)
        points.add(tail)
print("Answer 1 = ", len(list(points)))

points2 = set()
points2.add((0,0))
head2 = (0,0)
tails = [(0,0) for _ in range(9)]
for line in x:
    direction = line[0]
    distance = int(line[1:])
    for i in range(distance):
        head2 = updateHead(head2, direction)
        tails = updateTails(tails, head2)
        points2.add(tails[-1])

print("Answer 2 = ", len(list(points2)))

