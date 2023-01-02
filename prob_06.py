with open('inputs/input_06.txt','r') as f:
    m = f.read()

def getPacketStart(msg,k):
    for i in range(len(msg)-k+1):
        if(len(set(msg[i:i+k])) == k):
            #print(msg[i:i+k])
            return i + k
    return -1

print("Answer 1 =", getPacketStart(m,4))
print("Answer 2 =", getPacketStart(m,14))
