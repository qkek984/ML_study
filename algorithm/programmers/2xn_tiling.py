from collections import deque
def solution(n):
    if n ==0:
        return 0
    op=deque([0,1])
    answer = 1
    for i in range(1,n):
        answer += op[1]
        tmp = op[0]+op[1]
        op.append(tmp)
        op.popleft()
    return answer%1000000007
