from collections import deque
N,M,T = map(int,input().split())
arr = []
for _ in range(N):
    arr.append(deque(list(map(int,input().split()))))
command=[]

def rotation(mx,D,K):
    for _ in range(K%M):
        if D==0: #시계
            arr[mx-1].insert(0,arr[mx-1].pop())
        else:
            arr[mx-1].append(arr[mx-1].popleft())

dx,dy=(1,-1,0,0),(0,0,1,-1)
def clurstering():
    q = deque([])
    visited={}
    total = 0
    count = 0
    flag = True
    for i in range(N):
        for j in range(M):
            if arr[i][j]==0:
                continue
            total += arr[i][j]
            count += 1
            q.append((i,j))
            while q:
                x,y = q.popleft()
                num = arr[x][y]
                for d in range(4):
                    mx,my = x+dx[d],y+dy[d]
                    if my<0:
                        my=M-1
                    elif my>=M:
                        my=0
                    if (not 0<=mx<N) or (mx,my) in visited or arr[mx][my]==0:
                        continue
                    if arr[mx][my] == num:
                        q.append((mx,my))
                        visited[(mx,my)] = num
                        flag= False
    if flag:
        if total == 0:# 0인경우 예외처리
            return
        avg = total/count
        for i in range(N):
            for j in range(M):
                if arr[i][j] == 0:
                    continue
                if arr[i][j]>avg:
                    arr[i][j]-=1
                elif arr[i][j]<avg:
                    arr[i][j] +=1
    else:
        for x,y in visited:
            arr[x][y]=0

for _ in range(T):
    X,D,K = map(int,input().split())
    mul=1
    mx=X
    while mx<=N:
        rotation(mx,D,K)
        mul += 1
        mx = X * mul
    clurstering()

answer = 0
for a in arr:
    answer += sum(a)
print(answer)
