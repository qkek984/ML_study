from collections import deque
n, l, r = map(int, input().split())
place =[]
for _ in range(n):
    place.append(list(map(int, input().split())))

dx,dy=(1,-1,0,0),(0,0,1,-1)
answer = 0

while True:
    flag = False
    visited = [[False for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if visited[i][j]:
                continue
            visited[i][j] = True
            merge = [(i,j)]
            merge_num = place[i][j]
            q = deque([(i,j)])
            while q:
                x,y = q.popleft()
                for d in range(4):
                    mx, my = x+dx[d], y+dy[d]
                    if 0<=mx<n and 0<=my<n and visited[mx][my] == False:
                        if l<=abs(place[x][y] - place[mx][my])<=r:
                            merge.append((mx,my))
                            merge_num += place[mx][my]
                            visited[mx][my]= True
                            q.append((mx,my))
            if len(merge) > 1:
                flag = True
                merge_num = int(merge_num/len(merge))
                for x,y in merge:
                    place[x][y]= merge_num
    if flag:
        answer += 1
    else:
        break
print(answer)
