def solution(m, n, puddles):
    L = [[0]*(m+1) for i in range(n+1)]
    for pu in puddles:
        L[pu[1]][pu[0]] = -1
    for i in range(1,n+1):
        for j in range(1,m+1):
            if 1 == i == j:
                L[i][j] = 1
            elif L[i][j] == -1:
                L[i][j] = 0
            else:
                L[i][j] = (L[i-1][j]+L[i][j-1])%1000000007
    return L[-1][-1]
