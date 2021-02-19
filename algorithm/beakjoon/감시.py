n, m = map(int,input().split())
place = []
cctv = []
wall = 0

for i in range(n):
    tmp = list(map(int, input().split()))
    place.append(tmp)
    for j in range(m):
        if 1 <= tmp[j] <=5:
            cctv.append([i,j,tmp[j]])
        elif tmp[j]==6:
            wall += 1

dx,dy = (1,0,-1,0),(0,1,0,-1)
move = {1:[(0,),(1,),(2,),(3,)], 2:[(1,3),(0,2)], 3:[(0,1),(1,2),(2,3),(3,0)]
        , 4:[(3,0,1),(0,1,2),(1,2,3),(2,3,0)], 5:[(0,1,2,3)]}

vision = {}
for item in cctv:
    x,y,type = item
    for rotation in move[type]:
        tmp = set([])
        for r in rotation:
            mx, my = x, y
            while True:
                mx, my = mx + dx[r], my+dy[r]
                if 0<=mx<n and 0<=my<m and place[mx][my] != 6:
                    if place[mx][my] == 0:
                        tmp.add((mx,my))
                else:
                    break
        if (x,y) not in vision:
            vision[(x,y)] = [tmp]
        else:
            vision[(x,y)].append(tmp)

restPlace = n*m - len(cctv)- wall

def dfs(cctv, node):
    answer = n*m
    if not cctv:
        return restPlace-len(node)
    x,y,_ = cctv[0]
    for v in vision[(x,y)]:
        answer = min(answer, dfs(cctv[1:],node.union(v)))
    return answer

answer = dfs(cctv, set([]))

print(answer)
