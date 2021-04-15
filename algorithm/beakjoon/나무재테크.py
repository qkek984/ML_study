N,M,K = map(int,input().split())
A = []
place = []
for _ in range(N):
    A.append(list(map(int,input().split())))
    place.append([5 for _ in range(N)])
tree = {}
for _ in range(M):
    x,y,z = map(int,input().split())
    tree[(x-1,y-1)] = [z]

def spring():
    deathTree = {}
    spreadTree = {}
    for key in tree:
        x,y = key
        for i in range(len(tree[key])):
            z = tree[key][i]
            if place[x][y] >= z:
                place[x][y] -= z
                tree[key][i] += 1
                if tree[key][i]%5 == 0:
                    if key not in spreadTree:
                        spreadTree[key] = 1
                    else:
                        spreadTree[key] += 1
            else:
                deathTree[key]= tree[key][i:]
                tree[key] = tree[key][:i]
                break
    return tree,deathTree,spreadTree

def summer(deathTree):
    for key in deathTree:
        x,y = key
        for i in range(len(deathTree[key])):
            place[x][y] += deathTree[key][i]//2

dx,dy=(-1,-1,-1,0,0,1,1,1),(-1,0,1,-1,1,-1,0,1)
def fall(spreadTree):
    for key in spreadTree:
        x, y = key
        for d in range(8):
            mx, my = x + dx[d], y + dy[d]
            if 0 <= mx < N and 0 <= my < N:
                if (mx, my) not in tree:
                    tree[(mx, my)] = [1]*spreadTree[key]
                else:
                    tree[(mx, my)] = ([1]*spreadTree[key]) + tree[(mx, my)]

def winter():
    for i in range(N):
        for j in range(N):
            place[i][j] += A[i][j]

for _ in range(K):
    for i in range(4):
        if i==0:
            tree, deathTree,spreadTree = spring()
        elif i==1:
            summer(deathTree)
        elif i==2:
            fall(spreadTree)
        else:
            winter()

answer = 0
for key in tree:
    answer += len(tree[key])
print(answer)
