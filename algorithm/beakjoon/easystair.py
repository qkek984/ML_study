n = int(input())
dp=[0,1,1,1,1,1,1,1,1,1]
for iter in range(1,n):
    tmp=[0,0,0,0,0,0,0,0,0,0]
    for i in range(0,10):
        if dp[i] == 0:
            continue
        elif i==0:
            tmp[1] += dp[i]
        elif i == 9:
            tmp[8] += dp[i]
        else:
            tmp[i-1] += dp[i]
            tmp[i+1] += dp[i]
    dp = tmp
print(sum(dp)%1000000000)
