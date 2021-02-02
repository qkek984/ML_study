n = int(input())
stairs = [0,0,0]
for _ in range(n):
    stairs.append(int(input()))
dp = [0,0,0]
for i in range(3,n+3):
    dp.append(max(dp[i-2]+stairs[i], dp[i-3]+stairs[i-1]+stairs[i]))
    dp[-1] = max(dp[-1],dp[-2])
print(dp[-1])
