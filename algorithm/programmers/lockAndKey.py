import copy
def rotationKey(key,N):
    rotaKey = [[] for i in range(0,N)]
    for i in range(0,N):
        for j in range(N-1,-1,-1):  
            rotaKey[i].append(key[j][i])
    return rotaKey

def addPadding(lock,M,N):
    pLock=[]
    for i in range(0,M):
        pLock.append([0]*(N-1)+lock[i]+[0]*(N-1))
    for i in range(0,N-1):
        pLock.append([0]*len(pLock[0]))
        pLock.insert(0,[0]*len(pLock[0]))
    return pLock
    
def comp(pLock,key, i,j, N,M):
    tmp = copy.deepcopy(pLock)
    for x in range(0,N):
        for y in range(0,N):
            if tmp[i+x][j+y] == key[x][y]:
                if key[x][y] == 1:
                    return False
            else:
                tmp[i+x][j+y] = 1
    answer = 0
    for i in range(N-1,N+M-1):
        answer += sum(tmp[i][N-1:N+M-1])
    
    if M*M == answer:
        return True
    
def solution(key, lock):
    answer = False
    M = len(lock)
    N = len(key)
    keys=[]
    tmp = []
    for i in range(0,4):
        if i ==0:
            tmp = rotationKey(key,N)
        else:
            tmp = rotationKey(tmp,N)
        keys.append(tmp)
    pLock = addPadding(lock,M,N)

    for i in range(0,M+N-1):
        for j in range(0,M+N-1):
            for k in keys:
                if comp(pLock,k,i,j,N,M):
                    return True

    return answer
