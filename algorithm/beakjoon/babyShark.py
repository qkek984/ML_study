from collections import deque

N = int(input())
array=[]
for i in range(0,N):
    array.append(list(map(int,input().split())))

sp=None
for i in range(0,N):
    for j in range(0,N):
        if array[i][j] == 9:
            sp=(i,j)
            array[i][j] = 0
            break
    if sp != None:
        break
sharkSize=2
eat=0
time =0
dx,dy = (0,0,1,-1),(-1,1,0,0)
while True:
    minDist = 401
    minX = 21
    minY = 21
    visit = [[-1] * N for i in range(0, N)]
    visit[sp[0]][sp[1]] = 0
    q = deque()
    q.append((sp))
    while q:
        x, y = q.popleft()
        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            if nx<0 or nx>=N or ny<0 or ny>=N:
                continue
            elif visit[nx][ny] != -1 or array[nx][ny]>sharkSize:
                continue
            visit[nx][ny] = visit[x][y] + 1
            if array[nx][ny] != 0 and array[nx][ny] < sharkSize:
                if minDist > visit[nx][ny]:
                    minDist = visit[nx][ny]
                    minX = nx
                    minY = ny
                elif minDist == visit[nx][ny]:
                    if minX == nx:
                        if minY > ny:
                            minX = nx
                            minY = ny
                    elif minX > nx:
                        minX = nx
                        minY = ny
            q.append((nx,ny))

    if minDist != 401:
        time += minDist
        eat += 1
        if eat == sharkSize:
            eat=0
            sharkSize += 1
        array[minX][minY] = 0
        sp = (minX,minY)
    else:
        break
print(time)