n = int(input())
dp=[int(input())]
for i in range(2,n+1):
    num = list(map(int,input().split()))
    new_dp=[]
    for j in range(i):
        if j == 0:
            new_dp.append(num[j]+dp[j])
        elif j == i-1:
            new_dp.append(num[j] + dp[-1])
        else:
            new_dp.append(max(num[j]+dp[j-1],num[j]+dp[j]))
    dp = new_dp
print(max(dp))
