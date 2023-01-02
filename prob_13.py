from functools import cmp_to_key
def getInput():
    with open('inputs/input_13.txt', 'r') as f:
        lines = f.read().split('\n\n')
        lines = list(map(lambda x: list(map(eval, x.strip().split('\n'))), lines))
        return lines

def compare(a,b):
    ta = type(a)
    tb = type(b)
    #print(a,' vs ', b)
    if ta == int and tb == int:
        if a == b:
            return 0
        if a < b:
            return 1
        return -1
    if ta == int and tb == list:
        return compare([a], b)
    if ta == list and tb == int:
        return compare(a, [b])
    if ta == list and tb == list:
        la = len(a)
        lb = len(b)
        if la == 0 and lb != 0:
            return 1
        elif lb == 0 and la != 0:
            return -1
        elif lb == 0 and la == 0:
            return 0
        else:
            for i in range(min(la, lb)):
                lax = a[i]
                lbx = b[i]
                cx = compare(lax, lbx) 
                if cx != 0:
                    return cx
            if la < lb:
                return 1
            elif la == lb:
                return 0
            return -1

    else:
        print("FUCKED UP-TYPES")
        print(ta, tb)
        return 2
       

def part1():
    lines = getInput()
    total = 0
    ntotal = 0
    ll = len(lines)
    for i in range(ll):
        a = lines[i][0]
        b = lines[i][1]
        v = compare(a,b)
        if v == 1:
            total += i + 1
        if v == -1:
            ntotal += i + 1
    print("Answer 1 = ",total)

def part2():
    lines = getInput()
    new_lines = [] 
    for x in lines:
        new_lines += [x[0],x[1]]
    new_lines.append([[2]])
    new_lines.append([[6]])
    x1 = [[2]]
    x2 = [[6]]
    sort_lines = sorted(new_lines, reverse = True, key = cmp_to_key(compare))
    a = sort_lines.index(x1)
    b = sort_lines.index(x2)
    print("Answer 2 = ", (a+1)*(b+1))

part1()
part2()
