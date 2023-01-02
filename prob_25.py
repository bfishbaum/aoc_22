with open('inputs/input_25.txt','r') as f:
    lines = f.read().splitlines()

exp = '''\
1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122
'''


def SNAFUtoDec(n):
    total = 0
    for c in n:
        total *= 5
        if c == "2":
            total += 2
        elif c == "1":
            total += 1
        elif c == "0":
            total += 0
        elif c == "-":
            total -= 1
        elif c == "=":
            total -= 2
    return total

def DectoSnafu(d):
    snafu = ""
    while d != 0:
        m = d % 5
        r = d // 5
        if m == 0:
            snafu = "0" + snafu
        elif m == 1:
            snafu = "1" + snafu
        elif m == 2:
            snafu = "2" + snafu
        elif m == 3:
            snafu = "=" + snafu
            r += 1
        elif m == 4:
            snafu = "-" + snafu
            r += 1
        d = r
    return snafu

print("Answer 1 = ", DectoSnafu(sum([SNAFUtoDec(line) for line in lines])))
