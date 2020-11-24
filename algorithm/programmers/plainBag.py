N, K = map(int, input().split())
dp = [[0]* (K+1) for _ in range(N+1)]
for i in range(1,N+1):
    b_w, b_val = map(int, input().split())
    for j in range(1,K+1):
        idx = b_w + j
        if j < b_w:
            dp[i][j] = dp[i-1][j]
        else:
            dp[i][j] = max(b_val + dp[i-1][j-b_w], dp[i-1][j])
print(dp[-1][-1])
