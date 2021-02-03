num = int(input())

dp = [0,0,1,1]

for i in range(4,num+1):
    num1,num2=987654321,987654321
    if i%3 == 0:
        num1= dp[int(i/3)]+1
    if i%2 == 0:
        num2 = dp[int(i/2)]+1
    num3 = dp[i-1]+1
    dp.append(min(num1,num2,num3))
print(dp[num])