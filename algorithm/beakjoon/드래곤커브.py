n = int(input())
place = [[0 for _ in range(101)] for _ in range(101)]
dx,dy = (0,-1,0,1),(1,0,-1,0)
def draw(stack):
    tmp = []
    mx, my, _ = stack[-1]
    for i in range(len(stack)-1,0,-1):
        _,_,d = stack[i]
        d = (d + 1) % 4
        mx, my = mx+dx[d], my+dy[d]
        tmp.append((mx,my,d))
        place[mx][my]=1
    return tmp

for _ in range(n):
    y,x,d,g = map(int,input().split())
    stack =[(x,y,-1),(x+dx[d],y+dy[d],d)]
    place[x][y] = 1
    place[x+dx[d]][y+dy[d]] = 1
    for gi in range(g):
        stack.extend(draw(stack))

answer = 0
for i in range(100):
    for j in range(100):
        if place[i][j]==1 and place[i+1][j]==1 and place[i][j+1] == 1 and place[i+1][j+1]==1:
            answer += 1
print(answer)
