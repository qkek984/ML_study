def init(R, C, array=None):
    seaMap = [[None]*(C + 1) for j in range(0, R + 1)]
    if array:
        for i in range(0,len(array)):
            r, c, s, d, z = array[i]
            seaMap[r][c] = i
    return seaMap

def dChage(d):
    if d == 1:
        d = 2
    elif d == 2:
        d = 1
    elif d == 3:
        d = 4
    else:
        d = 3
    return d

def move(infoShark, R, C, M):
    dx, dy = (-1, 1, 0, 0), (0, 0, 1, -1)
    newShark = []
    seaMap = init(R, C)
    for i in range(0, M):
        r, c, s, d, z = infoShark[i]
        nr = (dx[d - 1] * s)
        nc = (dy[d - 1] * s)
        nr = r + (nr % ((R - 1) * 2))
        nc = c + (nc % ((C - 1) * 2))
        if nr > R:
            tmp = nr - R
            r = R - tmp
            if 0 >= r:
                r = abs(r) + 2
            else:
                d = dChage(d)
        else:
            r = nr

        if nc > C:
            tmp = nc - C
            c = C - tmp
            if 0 >= c:
                c = abs(c) + 2
            else:
                d = dChage(d)
        else:
            c = nc

        if seaMap[r][c]==None:
            newShark.append([r, c, s, d, z])
            seaMap[r][c] = len(newShark)-1
        else:
            sIndex = seaMap[r][c]
            if newShark[sIndex][4] < z:
                newShark[sIndex] = [r, c, s, d, z]

    return newShark, seaMap

R,C,M = map(int,input().split())
infoShark = []
answer=0
for i in range(0,M):
    infoShark.append(list(map(int, input().split())))

seaMap = init(R, C, array=infoShark)
for i in range(1,C+1):
    for j in range(1,R+1):
        if seaMap[j][i] != None:
            rIndex = seaMap[j][i]
            answer +=(infoShark.pop(rIndex))[4]
            M -= 1
            break
    infoShark, seaMap = move(infoShark,R,C,M)
    M = len(infoShark)

print(answer)