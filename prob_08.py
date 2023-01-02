with open('inputs/input_08.txt','r') as f:
    forest = f.read().splitlines()

forest = list(map(lambda x: list(map(lambda y: int(y), x)), forest))
xh = len(forest)
xw = len(forest[0])

bitmap = [[0] * xw for i in range(xh)]

def markByRow(forest, bitmap, row, right=False):
    line = forest[row]
    s = len(line)
    maxh = -1
    if (not right):
        for i in range(s):
            if line[i] > maxh:
                maxh = line[i]
                bitmap[row][i] = 1
    else:
        for i in range(s):
            if line[s-i-1] > maxh:
                maxh = line[s-i-1]
                bitmap[row][s-i-1] = 1
    return bitmap

def markByCol(forest, bitmap, col, up=False):
    s = len(forest)
    maxh = -1
    if (not up):
        for i in range(s):
            if forest[i][col] > maxh:
                maxh = forest[i][col]
                bitmap[i][col] = 1
    else:
        for i in range(s):
            if forest[s-i-1][col] > maxh:
                maxh = forest[s-i-1][col]
                bitmap[s-i-1][col] = 1
    return bitmap

def markBitMapAllWays(forest, bitmap):
    xh = len(forest)
    xw = len(forest[0])
    for i in range(xh):
        bitmap = markByRow(forest, bitmap, i, False)
        bitmap = markByRow(forest, bitmap, i, True)
    for j in range(xw):
        bitmap = markByCol(forest, bitmap, j, False)
        bitmap = markByCol(forest, bitmap, j, True)
    return bitmap

def markMapWithScore(forest,scoreMap,x,y):
    xh = len(forest)
    xw = len(forest[0])
    v = forest[x][y]
    tleft = 0
    for i in range(x+1,xh):
        tleft += 1
        if forest[i][y] >= v:
            break
    tright = 0
    for i in range(x-1,-1,-1):
        tright += 1
        if forest[i][y] >= v:
            break
    tdown = 0
    for j in range(y+1,xw):
        tdown += 1
        if forest[x][j] >= v:
            break
    tup = 0
    for j in range(y-1,-1,-1):
        tup += 1
        if forest[x][j] >= v:
            break

    scoreMap[x][y] = tleft * tright * tdown * tup
    return scoreMap

def markMapWithAllScores(forest):
    xh = len(forest)
    xw = len(forest[0])
    scoreMap = [[0] * xw for i in range(xh)]
    for x in range(xh):
        for y in range(xw):
            scoreMap = markMapWithScore(forest, scoreMap, x, y)
    return scoreMap

bitmap = markBitMapAllWays(forest, bitmap)

total = sum(list(map(lambda x: sum(x), bitmap)))
print("Answer 1 =",total)

scoreMap = markMapWithAllScores(forest)
best = max(list(map(lambda x: max(x), scoreMap)))
print("Answer 2 =",best)





