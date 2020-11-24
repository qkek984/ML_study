from collections import deque
button = [(3,1),(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2),(3,0),(3,2)]
dx,dy = (1,-1,0,0),(0,0,1,-1)
def distance(start,end):
    visited = [[False,False,False] for _ in range(4)]
    q = deque([(button[start][0],button[start][1],0)])
    while q:
        this = q.popleft()
        for i in range(4):
            mx,my = this[0]+dx[i],this[1]+dy[i]
            if mx < 0 or mx>3 or my < 0 or my>2 or visited[mx][my]:
                continue
            if (mx,my) == button[end]:
                return this[2]+1
            else:
                q.append((mx,my,this[2]+1))
def solution(numbers, hand):
    answer = ''
    left = 10
    right = 11
    for num in numbers:
        if num in [1,4,7] or num == left:
            answer +="L"
            left = num
            continue
        elif num in [3,6,9] or num == right:
            answer +="R"
            right = num
            continue
        l = distance(left,num)
        r = distance(right,num)
        if l == r:
            if hand=="right":
                answer +="R"
                right = num
            else:
                answer +="L"
                left = num
        elif l<r:
            answer +="L"
            left = num
        else:
            answer +="R"
            right = num
    return answer
