def parseLine(line):
    l2 = line.split(",")
    (p,q) = l2[0],l2[1]
    px = p.split("-")
    (p1,p2) = px[0],px[1]
    qx = q.split("-")
    (q1,q2) = qx[0],qx[1]
    return (int(p1),int(p2),int(q1),int(q2))

def contained(line):
    (p1,p2,q1,q2) = parseLine(line)
    return (p1 <= q1 and q2 <= p2) or (q1 <= p1 and p2 <= q2)

def overlap(line):
    (p1,p2,q1,q2) = parseLine(line)
    return not (q1 > p2 or p1 > q2)

with open('inputs/input_04.txt','r') as f:
    z = f.read().splitlines()

total_contained = 0
total_overlap = 0
for line in z:
    if(contained(line)):
        #print(line)
        #print(parseLine(line))
        total_contained += 1
    if(overlap(line)):
        total_overlap += 1

print("Answer 1 =", total_contained)
print("Answer 2 =", total_overlap)
