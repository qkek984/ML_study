from collections import deque
import copy
answer =[]
_place = [[] for _ in range(4)]
_fish = [[None] for _ in range(17)]
dx,dy = (0,-1,-1,0,1,1,1,0,-1),(0,0,-1,-1,-1,0,1,1,1)

for i in range(4):
    tmp = list(map(int, input().split(" ")))
    for j in range(0,len(tmp),2):
        _place[i].append([tmp[j],tmp[j+1]])
        _fish[tmp[j]]= [i,j//2]

def move(fish, place):
    for i in range(1, len(fish)):
        if not fish[i]:
            continue
        x,y = fish[i]
        for j in range(8):
            mx = x + dx[place[x][y][1]]
            my = y + dy[place[x][y][1]]
            if (mx < 0 or 3 < mx) or (my < 0 or 3 < my) or (place[mx][my][0] == -1):
                place[x][y][1] += 1
                if place[x][y][1] > 8:
                    place[x][y][1] = 1
                continue
            if place[mx][my][0] > 0:
                tmp = [place[mx][my][0],place[mx][my][1]]
                place[mx][my] = [place[x][y][0],place[x][y][1]]
                place[x][y] = tmp
                fish[i] = [mx ,my]
                fish[tmp[0]] = [x,y]
            elif place[mx][my][0] == 0:
                place[mx][my] = [place[x][y][0],place[x][y][1]]
                place[x][y] = [0,0]
                fish[i] = [mx, my]
            break

q = deque([[[0,0], _place, _fish, 0]])
while q:
    move_shark, place, fish, eaten = q.popleft()
    mx, my = move_shark
    aimfish = [place[mx][my][0], place[mx][my][1]]
    eaten += aimfish[0]
    fish[aimfish[0]] = None  # 먹힌 물고기 위치 갱신

    place[mx][my] = [-1, aimfish[1]] # 상어 이동
    if fish[0] != [None]:
        place[fish[0][0]][fish[0][1]] = [0,0]# 기존 상어 있던 자리 갱신
    fish[0] = [mx, my]  # 상어 위치 갱신
    move(fish, place)

    end = True
    d_idx = place[fish[0][0]][fish[0][1]][1]
    for i in range(3):
        mx = mx + dx[d_idx]
        my = my + dy[d_idx]
        if (mx < 0 or 3 < mx) or (my < 0 or 3 < my):
            break
        elif place[mx][my][0] > 0:
            end = False
            q.append([[mx,my],copy.deepcopy(place),copy.deepcopy(fish),eaten])
    if end:
        answer.append(eaten)

print(max(answer))
