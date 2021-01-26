n = int(input())
item =[0, 0]
dp =[0, 0]
for i in range(n):
    item.append(int(input()))
    dp.append(0)

answer = 0
for i in range(2,n+2):
    dp[i] = max(dp[i-3]+item[i-1]+item[i], dp[i-2]+item[i])
    dp[i] = max(dp[i-1],dp[i])
    answer = max(answer,dp[i])
print(answer)
