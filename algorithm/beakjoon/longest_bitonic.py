N = int(input())
bytonic = [0] + list(map(int,input().split()))
r_bytonic = [0] + list(reversed(bytonic))[:-1]
dp1, dp2 = [0]* (N+1),[0]* (N+1)

for i in range(1,N+1):
    for j in range(1,i):
        if bytonic[i] > bytonic[j]:
            dp1[i] = max(dp1[i], dp1[j])
        if r_bytonic[i] > r_bytonic[j]:
            dp2[i] = max(dp2[i], dp2[j])
    dp1[i] += 1
    dp2[i] += 1

answer = 0
for d1,d2 in zip(dp1[1:],list(reversed(dp2))[:-1]):
    answer = max(answer, d1+d2-1)
print(answer)
