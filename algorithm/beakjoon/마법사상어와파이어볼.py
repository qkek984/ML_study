from collections import deque
N,M,K = map(int,input().split())
q= deque([])
for _ in range(M):
    q.append(list(map(int,input().split())))

dx,dy =(-1,-1,0,1,1,1,0,-1),(0,1,1,1,0,-1,-1,-1)

for _ in range(K):
    moved_fbs={}
    while q:
        r, c, m, s, d = q.popleft()
        r = (r + s * dx[d]) % N
        c = (c + s * dy[d]) % N
        if (r,c) not in moved_fbs:
            moved_fbs[(r, c)] = [(m, s, d)]
        else:
            moved_fbs[(r, c)].append((m, s, d))

    for fbs in moved_fbs:
        len_fbs = len(moved_fbs[fbs])
        r, c = fbs
        if len_fbs == 1:
            m,s,d = moved_fbs[fbs][0]
            q.append((r,c,m,s,d))
        else:
            sum_msd=[0,0,[]]
            for fb in moved_fbs[fbs]:
                m,s,d = fb
                sum_msd[0] += m
                sum_msd[1] += s
                sum_msd[2].append(d%2)
            m = int(sum_msd[0]/5)
            s = int(sum_msd[1] / len_fbs)
            if m == 0:
                continue
            if sum_msd[2].count(0) == len_fbs or sum_msd[2].count(1)== len_fbs:
                d = [0,2,4,6]
            else:
                d = [1,3,5,7]
            for item in d:
                q.append((r,c,m,s,item))
answer = 0
while q:
    _,_,m,_,_ = q.popleft()
    answer += m
print(answer)
