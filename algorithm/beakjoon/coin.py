n,k = list(map(int,input().split()))
coins=[]
for i in range(n):
    coins.append(int(input()))

sum_vals = set([0])
idx = 1
while True:
    check_min = k+1
    tmp = set([])
    for coin in coins:
        for sum_val in sum_vals:
            result = sum_val + coin
            if k == result:
                print(idx)
                exit()
            elif k > result:
                tmp.add(result)
            check_min = min(check_min,result)
    if check_min > k:
        break
    sum_vals = tmp
    idx +=1
print(-1)
