from collections import deque
from itertools import combinations
import copy
answer=0
N,M= map(int, input().split())
array=[]
for i in range(N):
    array.append(list(input().split()))

zeroSpace=[]
virus=[]
for i in range(N):
    for j in range(M):
        if array[i][j]== '0':
            zeroSpace.append((i,j))
        if array[i][j]== '2':
            virus.append((i,j))
comb=[]
items = [str(i) for i in range(0,len(zeroSpace))]
tmp = list(map(' '.join, combinations(items,3)))
for i in tmp:
    c= i.split()
    comb.append((int(c[0]),int(c[1]),int(c[2])))

dx,dy=(1,-1,0,0),(0,0,1,-1)

for com in comb:
    ax, ay = zeroSpace[com[0]]
    bx, by = zeroSpace[com[1]]
    cx, cy = zeroSpace[com[2]]
    tarray = copy.deepcopy(array)
    tarray[ax][ay] = '1'
    tarray[bx][by] = '1'
    tarray[cx][cy] = '1'

    q=deque()
    for i in virus:
        q.append(i)

    while q:
        tmpVirus = q.popleft()
        xx = tmpVirus[0]
        yy = tmpVirus[1]
        for i in range(4):
            x = xx+dx[i]
            y = yy+dy[i]
            if 0<=x and x<N and 0<=y and y<M:
                if tarray[x][y]=='0':
                    tarray[x][y]='2'
                    q.append((x,y))

    count=0
    for i in range(N):
        for j in range(M):
            if tarray[i][j]=='0':
                count += 1
    if answer<count:
        answer=count

print(answer)

