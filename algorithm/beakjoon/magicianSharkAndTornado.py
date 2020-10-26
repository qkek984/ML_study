place = []
N = int(input())
for _ in range(N):
    place.append(list(map(int,input().split(" "))))
dx,dy=(1,0,-1,0),(0,1,0,-1)
rotation=[1, 2, 2, 3]
position=(N//2, (N//2)-1)
move_command=[(0,1,3),(1,2,0),(2,1,3),(3,2,0)]
def move(d,start):
    origin = place[start[0]][start[1]]
    moved = 0
    out = 0

    visited = []
    visited.append((start[0],start[1]))
    place[start[0]][start[1]] = 0
    command = move_command[d]

    for com in command:
        x, y = start
        x, y = x + dx[com], y + dy[com]
        if d != com:
            if (0 <= x and x<N) and (0 <= y and y<N):
                place[x][y] += (origin * 7)//100
                moved += (origin * 7)//100
            else:
                out += (origin * 7)//100
                moved += (origin * 7) // 100
        visited.append((x, y))

        for i in range(4):
            mx, my = x + dx[i], y + dy[i]
            if (mx, my) in visited:
                continue
            elif d == com:
                weight = 5 if com == i else 10
            else:
                weight = 2 if com == i else 1

            if (0 <= mx and mx < N) and (0 <= my and my < N):
                place[mx][my] += (origin * weight) // 100
            else:
                out += (origin * weight) // 100
            moved += (origin * weight) // 100
            visited.append((mx, my))

    if (0 <= start[0]+dx[d] and start[0]+dx[d] < N) and (0 <= start[1]+dy[d] and start[1]+dy[d] < N):
        place[start[0]+dx[d]][start[1]+dy[d]] += (origin-moved)
    else:
        out += (origin-moved)
    return out

out = 0
out += move(3,position)
while position != (0,-1):
    mx, my = position
    for i in range(4):
        for _ in range(rotation[i]):
            mx,my = mx+ dx[i], my+dy[i]
            if my != -1:
                out += move(i,(mx,my))
        rotation[i] += 2
    position = (mx,my)

print(out)
