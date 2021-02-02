#1 1 2 4 7 12
##1 2 3 5 9 16

T = int(input())
dp=[0,1,1,1]+[0]*97
for i in range(4,101):
    dp[i] = dp[i-2]+dp[i-3]

for _ in range(T):
    print(dp[int(input())])
