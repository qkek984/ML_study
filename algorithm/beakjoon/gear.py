gear=[]
for i in range(0,4):
    tmp = input().split()
    g=[]
    for t in tmp[0]:
        g.append(int(t))
    gear.append(g)
K=int(input())
operation = []
for i in range(0,K):
    operation.append(list(map(int,input().split())))
def rotation(array, d):
    newArray=[]
    if d == 1:
        newArray = [array[-1]] + array[0:-1]
    else:
        newArray = array[1:]+[array[0]]
    return newArray
def reverse(d):
    if d == 1:
        return -1
    else:
        return 1

score = [1,2,4,8]
answer = 0
for i in range(0,K):
    other=[False, False, False]
    g = operation[i][0]-1
    d = operation[i][1]
    if gear[0][2] != gear[1][6]:
        other[0] = True
    if gear[1][2] != gear[2][6]:
        other[1] = True
    if gear[2][2] != gear[3][6]:
        other[2] = True
    gear[g] = rotation(gear[g], d)
    if g == 0:
        if other[0]==True:
            gear[1] = rotation(gear[1], reverse(d))
            if other[1] == True:
                gear[2] = rotation(gear[2], d)
                if other[2] == True:
                    gear[3] = rotation(gear[3], reverse(d))
    elif g == 1:
        if other[0]==True:
            gear[0] = rotation(gear[0], reverse(d))
        if other[1]==True:
            gear[2] = rotation(gear[2], reverse(d))
            if other[2] == True:
                gear[3] = rotation(gear[3], d)
    elif g == 2:
        if other[1]==True:
            gear[1] = rotation(gear[1], reverse(d))
            if other[0] == True:
                gear[0] = rotation(gear[0], d)
        if other[2]==True:
            gear[3] = rotation(gear[3], reverse(d))
    else:
        if other[2]==True:
            gear[2] = rotation(gear[2], reverse(d))
            if other[1] == True:
                gear[1] = rotation(gear[1], d)
                if other[0] == True:
                    gear[0] = rotation(gear[0], reverse(d))
for i in range(0,4):
    if gear[i][0] == 1:
        answer += score[i]
print(answer)


