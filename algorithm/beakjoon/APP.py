N,M = map(int, input().split())
m = [0]+list(map(int, input().split()))
c = [0]+list(map(int, input().split()))
sum_c=sum(c)+1

answer = sum(c)+1
dp = [[0 for _ in range(sum_c)] for __ in range(N+1)]
for i in range(1,N+1):
    w,v = m[i],c[i]
    for j in range(0,sum_c):
        if v<=j:
            dp[i][j] = max(w + dp[i-1][j-v], dp[i-1][j])
        else:
            dp[i][j] = dp[i-1][j]
        if dp[i][j]>=M:
            answer = min(answer,j)
print(answer)
for i in dp:
    print(i)

