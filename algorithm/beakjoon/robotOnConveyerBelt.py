N,K= map(int,input().split())
arr =[]
step = 0
zero = 0
for ar in list(map(int,input().split())):
    arr.append([False, ar])
    if ar == 0:
        zero += 1
while zero < K:
    arr.insert(0,arr.pop())
    arr[N][0] = False
    arr[N-1][0] = False
    for i in range(N-2,-1,-1):
        if arr[i][0]:
            m_idx = i+1
            if arr[m_idx][0]== False and arr[m_idx][1] != 0:
                arr[i][0] = False
                arr[m_idx][0]= True
                arr[m_idx][1] -= 1
                if arr[m_idx][1] == 0:
                    zero += 1
    if arr[0][0] == False and arr[0][1] != 0:
        arr[0][0] = True
        arr[0][1] -= 1
        if arr[0][1] == 0:
            zero += 1
    step += 1
print(step)
