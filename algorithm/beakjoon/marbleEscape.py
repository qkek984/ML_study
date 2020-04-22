from collections import deque

N,M = map(int, input().split())
array=[]
check = [[[[False] * M for _ in range(N)] for _ in range(M)] for _ in range(N)]

for i in range(N):
    array.append(input())

def init():
    for i in range(0,N):
        for j in range(0,M):
            if "B" == array[i][j]:
                array[i] = array[i][0:j]+"."+array[i][j+1:]
                B = (i,j)
            elif "R" == array[i][j]:
                array[i] = array[i][0:j] + "." + array[i][j + 1:]
                R = (i,j)
            elif "O" == array[i][j]:
                O = (i,j)
    return B,R,O

def bfs(B,R,O,array):
    dx,dy=(-1,1,0,0),(0,0,-1,1)
    q = deque()
    q.append((R[0],R[1],B[0],B[1],1))
    check[R[0]][R[1]][B[0]][B[1]] = True
    while q:
        rx, ry, bx, by, depth = q.popleft()
        if depth>10:
            print("-1")
            return
        for i in range(4):
            new_rx, new_ry, r_count = move(array,rx,ry,dx[i],dy[i])
            new_bx, new_by, b_count = move(array,bx,by,dx[i],dy[i])
            if O == (new_bx, new_by):
                continue
            elif O == (new_rx, new_ry):
                print(depth)
                return
            if (new_rx, new_ry) == (new_bx, new_by):
                if r_count > b_count:
                    new_rx -= dx[i]
                    new_ry -= dy[i]
                else:
                    new_bx -= dx[i]
                    new_by -= dy[i]
            if not check[new_rx][new_ry][new_bx][new_by]:
                check[new_rx][new_ry][new_bx][new_by] = True
            q.append((new_rx, new_ry, new_bx, new_by, depth+1))
    print("-1")

def move(array, x, y, dx, dy):
    count=0
    while array[x+dx][y+dy] != "#":
        x = x + dx
        y = y + dy
        count += 1
        if array[x][y] == "O":
            break
    return x,y,count

B,R,O = init()
bfs(B,R,O,array)