M,N = map(int,input().split())
arr = []
for _ in range(M):
    arr.append(list(map(int,input().split())))
dx,dy = (-1,1,0,0),(0,0,-1,1)
visited = [[-1 for _ in range(N)] for __ in range(M)]

def dfs(x,y):
    if (x,y) == (M-1,N-1):
        return 1
    elif visited[x][y] != -1:
        return visited[x][y]
    else:
        visited[x][y] = 0

    for i in range(4):
        mx,my = x+dx[i], y+dy[i]
        if mx<0 or mx >= M or my<0 or my >= N or arr[x][y] <= arr[mx][my]:
            continue
        else:
            visited[x][y] += dfs(mx,my)
    return visited[x][y]

answer = dfs(0,0)
print(answer)
