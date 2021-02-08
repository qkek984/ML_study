from collections import deque

def cal(n):
    N = 1
    for _ in range(n):
        N = N * 2
    return N

n,q = map(int,input().split())
N = cal(n)

arr = []
for _ in range(N):
    arr.append(list(map(int,input().split())))
L = list(map(int,input().split()))

def rotation(arr,mx):
    newArr = [[[] for _ in range(int(N/mx))] for __ in range(int(N/mx))]
    for i in range(0,N,mx):
        for j in range(0,N,mx):
            for k in range(0,mx):
                newArr[int(i/mx)][int(j/mx)].append(arr[i+k][j:j + mx])

    newArr2 = [[[[] for _ in range(mx)] for _ in range(int(N / mx))] for __ in range(int(N / mx))]

    for i in range(len(newArr)):
        for j in range(len(newArr[i])):
            for ii in range(len(newArr[i][j])):
                for jj in range(len(newArr[i][j][ii])):
                    newArr2[i][j][jj].insert(0,newArr[i][j][ii][jj])

    result = [[]for _ in range(N)]
    for i in range(len(newArr2)):
        for j in range(len(newArr2[i])):
            for k in range(len(newArr2[i][j])):
                result[k+(i*mx)].extend(newArr2[i][j][k])

    return result

dx,dy=(0,0,1,-1),(1,-1,0,0)

for l in L:
    mx = cal(l)
    arr = rotation(arr, mx)

    visited = [[False for _ in range(N)] for __ in range(N)]
    newArr = [[0 for _ in range(N)] for __ in range(N)]
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            if visited[i][j] or arr[i][j] == 0:
                continue
            q = deque([(i,j)])
            while q:
                x,y = q.popleft()
                visited[x][y] = True
                count = 4
                for d in range(4):
                    mx,my = x+dx[d], y+dy[d]
                    if 0<=mx<N and 0<=my<N and arr[mx][my] != 0:
                        if visited[mx][my]:
                            pass
                        else:
                            q.append((mx,my))
                            visited[mx][my]= True
                    else:
                        count -= 1

                if count >= 3:
                    newArr[x][y] = arr[x][y]
                else:
                    newArr[x][y] = arr[x][y]-1
    arr = newArr
answer = 0
visited = [[False for _ in range(N)] for __ in range(N)]
max_cluster =0

for i in range(len(arr)):
    for j in range(len(arr[i])):
        if arr[i][j]==0 or visited[i][j]:
            continue
        cluster = 1
        q = deque([(i,j)])
        while q:
            x,y = q.popleft()
            visited[x][y]= True
            for d in range(4):
                mx,my = x+dx[d], y+dy[d]
                if 0<=mx<N and 0<=my<N and visited[mx][my]==False:
                    if arr[mx][my] >0:
                        cluster +=1
                        visited[mx][my]=True
                        q.append((mx,my))
        max_cluster = max(max_cluster, cluster)

for a in arr:
    answer += sum(a)
print(answer)
print(max_cluster)
