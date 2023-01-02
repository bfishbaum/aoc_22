with open('inputs/input_02.txt','r') as f:
    z = f.read().splitlines()

def getScoreV1(opp, you):
    total = 0
    if(you == "X"):
        total += 1
        if (opp == "A"):
            return total + 3
        if (opp == "B"):
            return total + 0
        if (opp == "C"):
            return total + 6
    if(you == "Y"):
        total += 2
        if (opp == "A"):
            return total + 6
        if (opp == "B"):
            return total + 3
        if (opp == "C"):
            return total + 0
    if(you == "Z"):
        total += 3
        if (opp == "A"):
            return total + 0
        if (opp == "B"):
            return total + 6
        if (opp == "C"):
            return total + 3
    return total

def getScoreV2(opp, you):
    total = 0
    if(you == "X"):
        total += 0
        if (opp == "A"):
            return total + 3
        if (opp == "B"):
            return total + 1
        if (opp == "C"):
            return total + 2
    if(you == "Y"):
        total += 3
        if (opp == "A"):
            return total + 1
        if (opp == "B"):
            return total + 2
        if (opp == "C"):
            return total + 3
    if(you == "Z"):
        total += 6
        if (opp == "A"):
            return total + 2
        if (opp == "B"):
            return total + 3
        if (opp == "C"):
            return total + 1
    return total


totalv1 = 0
totalv2 = 0
for line in z:
    opp = line[0]
    you = line[2]
    t1 = getScoreV1(opp, you)
    totalv1 += t1
    t2 = getScoreV2(opp, you)
    totalv2 += t2
    #print(opp, you, t, total)
print("Answer 1 =", totalv1)
print("Answer 2 =", totalv2)


