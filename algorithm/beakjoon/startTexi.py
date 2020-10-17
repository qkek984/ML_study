from collections import deque
N,M,gas = map(int,input().split(" "))
place=[]
for _ in range(N):
    place.append(list(map(int,input().split(" "))))
texi = list(map(int,input().split(" ")))
texi = (texi[0]-1, texi[1]-1)

passengers={}
homes={}
for i in range(M):
    info = list(map(int,input().split(" ")))
    passengers[(info[0]-1, info[1]-1)] = i

    if (info[2]-1, info[3]-1) in homes:
        homes[(info[2]-1, info[3]-1)].append(i)
    else:
        homes[(info[2] - 1, info[3] - 1)]=[i]

dx,dy=(1,-1,0,0),(0,0,1,-1)

def find_passenger(tx, ty, gas):
    if (tx,ty) in passengers:
        return (0, tx, ty)
    visited = [[False for _ in range(N)] for __ in range(N)]
    visited[tx][ty]= True
    priority=[]
    q = deque([(tx, ty, 0)])
    while q:
        if len(priority) == len(passengers):
            break
        x,y,dist = q.popleft()
        for i in range(4):
            mx, my = x+dx[i], y+dy[i]
            if (mx<0 or N <= mx) or (my<0 or N <= my):
                continue
            elif visited[mx][my] or place[mx][my] == 1:
                continue
            elif 1 > gas-dist:
                continue
            if (mx,my) in passengers:
                priority.append((dist+1,mx,my))
                visited[mx][my]= True
                q.append((mx,my,dist+1))
            else:
                visited[mx][my] = True
                q.append((mx, my, dist + 1))
    if priority:
        priority = sorted(priority,key=lambda x:(x[0],x[1],x[2]))
        return priority[0]
    else:
        return False

def find_home(px, py, gas):
    if (px, py) in homes and passengers[(px, py)] in homes[(px, py)]:
        return (0, px, py)
    visited = [[False for _ in range(N)] for __ in range(N)]
    visited[px][py]= True
    q = deque([(px, py, 0)])
    while q:
        x,y,dist = q.popleft()
        for i in range(4):
            mx, my = x+dx[i], y+dy[i]
            if (mx<0 or N <= mx) or (my<0 or N <= my):
                continue
            elif visited[mx][my] or place[mx][my] == 1:
                continue
            elif 1 > gas-dist:
                continue
            if (mx,my) in homes and passengers[(px,py)] in homes[(mx,my)]:
                return (dist+1, mx, my)
            else:
                visited[mx][my] = True
                q.append((mx, my, dist + 1))
    return False

for i in range(M):
    passenger = find_passenger(texi[0], texi[1], gas)
    if passenger:
        gas -= passenger[0]
    else:
        gas = -1
        break
    home = find_home(passenger[1],passenger[2],gas)
    if home:
        gas -= home[0]
    else:
        gas = -1
        break

    if gas >= 0:
        gas += (home[0] * 2)
        texi = (home[1],home[2])
        del passengers[(passenger[1],passenger[2])]
    else:
        gas = -1
        break

print(gas)
