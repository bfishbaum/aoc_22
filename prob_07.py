import re


# str -> size, parent, directories
# everything use full root name

def goUp(path):
    if (path == ""):
        return ""
    return "/".join(path.split('/')[:-1]) 

def updateFileSizes(fs, cd, fl):
    size = fs[fl][0]
    #print("Starting update", cd, size, fl)
    while cd != "":
        fs[cd] = (fs[cd][0] + size, fs[cd][1])
        #print("Updating", cd, size, fs[cd])
        cd = goUp(cd)
    fs[""] = (fs[""][0] + size, fs[""][1])
    #print("Finished update")
    return fs

#def updateAllFilesSizes(fs):

def processLines(lines):
    fs = {"":(0,[])}
    cd = ""
    c = 0;
    while (c < len(lines)):
        line = lines[c]
        if (line.startswith("$ ls")):
            c += 1
            continue
            
        elif (line.startswith("$ cd")):
            c += 1
            newdir = line[5:]
            if newdir == "..":
                cd = goUp(cd)
                continue
            elif newdir.startswith("/"):
                cd = ""
            else:
                cd = cd + "/" + newdir
                if cd not in fs:
                    fs[cd] = (0, [])
                    print("shouldn't be happening")
                    x = 1/0
                continue

        elif (line.startswith("dir ")):
            c += 1
            newdir = cd + "/" + line[4:]
            if (newdir not in fs[cd][1]):
                fs[cd] = (fs[cd][0], fs[cd][1] + [newdir])
                if newdir not in fs:
                    fs[newdir] = (0, [])
            continue

        else:
            match = re.fullmatch(r"([0-9]+) ([\w\.]+)", line)
            if match != None:
                size = match.group(1)
                name = match.group(2)
                fullname = cd + "/" + name

                if fullname not in fs:
                    if (fullname not in fs[cd][1]):
                        fs[cd] = (fs[cd][0], fs[cd][1] + [fullname])
                    fs[fullname] = (int(size),[]) 
                    fs = updateFileSizes(fs, cd, fullname)
            else:
                print("oops! ", line)
            c += 1
            continue
    #print(fs)
    return fs


with open('inputs/input_07.txt','r') as f:
    lines = f.read().splitlines()

fs = processLines(lines)

def checkFS(fs):
    for p in fs.keys():
        size = fs[p][0]
        subs = fs[p][1]
        if fs[p][1] != []:
            t = 0
            for k in subs:
                t += fs[k][0]
            if t != size:
                print(p, "calc: ", t, "listed: ",size, subs)
        else:
            print(p, fs[p])



total = 0
for p in fs.keys():
    if fs[p][0] <= 100000 and fs[p][1] != []:
        total += fs[p][0]

print("Answer 1 =", total)
total_fs_size = 70000000
req_size = 30000000

size_left = total_fs_size - fs[''][0]
min_to_del = req_size - size_left
#print(size_left, min_to_del)

best = total_fs_size
best_dir = ''
for p in fs.keys():
    s = fs[p][0]
    if s >= min_to_del and s < best and fs[p][1] != []:
        best = s
        best_dir = p

print("Answer 2 =", best)




