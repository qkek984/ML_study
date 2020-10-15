N,M,K = map(int,input().split(" "))
place = []
shark = [[] for _ in range(M + 1)]
shark_smell = [[None for __ in range(K-1)] for _ in range(M + 1)]
for i in range(N):
    row = list(map(int,input().split(" ")))
    for j in range(N):
        if row[j] > 0:
            shark[row[j]]=(i, j)
            shark_smell[row[j]].append((i, j))
    place.append(row)
D = [0]+list(map(int,input().split(" ")))
priority = [[] for _ in range(M+1)]
for i in range(1, M+1):
    for j in range(4):
        priority[i].append(tuple(map(int,input().split(" "))))
dx,dy = (None,-1,1,0,0),(None,0,0,-1,1)

s=0
shark_count = M
while s<1000:
    update = {}
    for i in range(1,M+1):
        if shark[i] == False:
            continue
        x,y = shark[i]
        #####
        d_idx = D[i]-1
        smell_d = None
        new_d = None
        mx,my = None, None
        for j in range(4):
            new_d = priority[i][d_idx][j]
            mx, my = x + dx[new_d], y + dy[new_d]
            if (mx < 0 or N <= mx) or (my < 0 or N <= my):
                continue
            elif place[mx][my] > 0:
                if place[mx][my] == i:
                    if smell_d == None:
                        smell_d = new_d
                continue
            D[i] = new_d
            break
        else:
            D[i] = smell_d
            mx, my = x + dx[smell_d], y + dy[smell_d]

        ###
        if not (mx,my) in update:
            update[(mx,my)] = i
        else:
            shark[i] = False
            shark_count -= 1

    for i in range(1,M+1):
        if shark_smell[i]:
            del_xy = shark_smell[i].pop(0)
            if del_xy:
                place[del_xy[0]][del_xy[1]] = 0
    for xy in update:
        s_idx = update[xy]
        shark[s_idx] = xy
        if xy in shark_smell[s_idx]:
            remove_idx = shark_smell[s_idx].index(xy)
            shark_smell[s_idx][remove_idx] = None
        shark_smell[s_idx].append(xy)
        place[xy[0]][xy[1]] = s_idx

    s += 1
    if shark_count == 1:
        break
if shark_count != 1:
    print(-1)
else:
    print(s)
