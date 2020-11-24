from collections import deque
def solution(board):
    len_board = len(board)
    board[0][0] = 1
    cost = [[0]*len_board for _ in range(len_board)]
    cost[0][0] = -500
    dx,dy = (1,-1,0,0),(0,0,1,-1)
    q = deque([(0,0,-1,-500)])
    while q:
        x, y, d, c = q.popleft()
        if c != cost[x][y]:
            continue
        for i in range(4):
            mx,my = x+dx[i], y+dy[i]
            if mx<0 or mx>=len_board or my<0 or my>=len_board or board[mx][my]==1:
                continue
            op = 100 if d == i else 600
            if cost[mx][my] == 0:
                cost[mx][my] = cost[x][y]+op
                q.append((mx,my,i,cost[mx][my]))
            elif cost[mx][my] >= cost[x][y]+op:
                cost[mx][my] = cost[x][y]+op
                q.append((mx,my,i,cost[mx][my]))
    return cost[-1][-1]
