def binary(A):
    front =0
    rear = len(A)-1
    half = 0
    while front < rear:
        half = (rear+front)//2
        if A[half] == 1:
            break
        elif A[half] < 1:
            front = half+1
            half += 1
        else:
            rear = half-1
            half -= 1
    if A[half] == 1:
        return half
    else:
        return -1

def solution(A):
    # write your code in Python 3.6
    A= list(set(A))
    A.sort()
    idx = binary(A)
    if idx == -1:
        return 1
    else:
        A = A[idx:]
    answer = A[-1]+1
    for i in range(1,len(A)):
        if A[i-1]+1 != A[i]:
            answer = A[i-1]+1
            break
    return answer