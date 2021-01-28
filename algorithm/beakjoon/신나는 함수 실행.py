m = {}
def w(a,b,c):
    if a<=0 or b<=0 or c<=0:
        return 1
    if a > 20 or b>20 or c>20:
        return w(20, 20, 20)

    if (a,b,c) in m:# 메모제이션
        return m[(a,b,c)]

    if a<b<c:
        m[(a, b, c)] = w(a, b, c - 1) + w(a, b - 1, c - 1) - w(a, b - 1, c)
        return m[(a, b, c)]
    else:
        m[(a,b,c)] = w(a-1,b,c)+w(a-1,b-1,c)+w(a-1,b,c-1) - w(a-1,b-1,c-1)
        return m[(a,b,c)]

while True:
    a,b,c = map(int,input().split())
    if (a,b,c) == (-1,-1,-1):
        break
    print("w(%d, %d, %d) = %d"%(a, b, c, w(a, b, c)))
