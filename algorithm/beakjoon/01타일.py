'''
1 1
2 00 11
3 100 001 111
4 0000 1001 0011 1100 1111
5 00001 10000 00100 11001 1 0011 00111 11100 11111
'''
import sys
input = sys.stdin.readline
n = int(input())
dp = [1,2]
for i in range(3,n+1):
    dp = [dp[1],(dp[0]+dp[1])%15746]
if n==1:
    print(1)
else:
    print(dp[-1])




'''
from itertools import combinations_with_replacement
from itertools import permutations
item = ["00","1"]
arr =set([])
for i in range(10):
    comb = permutations(item,i)
    print(list(comb))
    for c in comb:
        tmp=""
        for num in c:
            tmp += num
        arr.add(tmp)

print(arr)
length = [0 for i in range(7)]
print(length)
for a in arr:
    lena = len(a)
    if 0<lena<7:
        length[lena] += 1

print(length)
'''


#answer%15746