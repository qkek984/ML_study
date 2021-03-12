n = int(input())
k = int(input())
place =[[0 for _ in range(n)] for _ in range(n)]
for _ in range(k):
    x,y = map(int,input().split())
    place[x-1][y-1] = 2
l= int(input())
rotate = {}
for _ in range(l):
    s , rd = input().split()
    rotate[int(s)] = rd
dx,dy = (0,1,0,-1),(1,0,-1,0)
change_d = {0:(3,1), 1:(0,2), 2:(1,3), 3:(2,0)}
place[0][0] = 1
q = [(0,0)]
d = 0

answer = 0
while answer < 10001:
    answer += 1
    x,y = q[-1]
    mx,my = x+dx[d],y+dy[d]
    if 0<=mx<n and 0<=my<n:
        if place[mx][my] == 2:
            place[mx][my] = 1
            q.append((mx,my))
        elif place[mx][my] == 0:
            place[mx][my] = 1
            q.append((mx, my))
            del_x,del_y = q.pop(0)
            place[del_x][del_y] = 0
        else:
            break
    else:
        break
    if answer in rotate:
        rd = rotate[answer]
        if rd == 'L':
            d = change_d[d][0]
        else:
            d = change_d[d][1]
print(answer)
