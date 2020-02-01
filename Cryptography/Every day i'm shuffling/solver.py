from random import *

def Shuffle(p, data):
    buf = list(data)
    for i in range(len(data)):
        buf[i] = data[p[i]]
    return ''.join(buf)

file_name = 'fsegovs_meaoerbma_'

data = open(file_name + '.txt', 'r').read()

s = 1

while s <= len(file_name):
    name = list('message_from_above')
    seed(s)
    shuffle(name)
    if ''.join(name) == file_name:
        break
    s += 1

print(s)

t = list(range(len(data)))
shuffle(t)
p = list(range(len(data)))

for i, j in enumerate(t):
    p[j] = i

data = Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,data))))))))))))))))))))))))))))))))))))))))

print(data)
