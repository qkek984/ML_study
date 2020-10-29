N = int(input())
arr = [[0,0]]
for i in range(N):
    arr.append(list(map(int,input().split())))
arr.sort(key=lambda x:(x[0],x[1]))
dp=[0]*(N+1)
for i in range(1,N+1):
    for j in range(i-1,0,-1):
        if arr[i][1] > arr[j][1]:
            dp[i] = max(dp[i], dp[j])
    dp[i] += 1
print(N - max(dp))
