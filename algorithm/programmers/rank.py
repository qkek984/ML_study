from collections import deque
def solution(n, results):
    answer = 0
    win = [set([]) for _ in range(n+1)]
    lose = [set([]) for _ in range(n+1)]
    for result in results:
        winner = result[0]
        loser = result[1]
        win[winner].add(loser)
        lose[loser].add(winner)

    for i in range(1, n+1):
        q= deque(list(win[i]))
        tmp=[]
        while q:
            this = q.popleft()
            for wi in win[this]:
                if not wi in tmp:
                    tmp.append(wi)
                    q.append(wi)
        win[i]= set(list(win[i])+tmp)
        #####
        q= deque(list(lose[i]))
        tmp=[]
        while q:
            this = q.popleft()
            for lo in lose[this]:
                if not lo in tmp:
                    tmp.append(lo)
                    q.append(lo)
        lose[i]= set(list(lose[i])+tmp)

    for i in range(1, n+1):
        if n-1 == (len(win[i])+len(lose[i])):
            answer += 1
    return answer
