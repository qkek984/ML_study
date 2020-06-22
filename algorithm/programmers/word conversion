from collections import deque
def solution(begin, target, words):
    answer = 0
    len_w = len(begin)
    q = deque([(begin,0)])
    while q:
        w = q.popleft()
        if w[0] == target:
            answer = w[1]
            break
        i = 0
        m = 0
        index = 0
        while index < len(words):
            dif = 0
            for j in range(0, len_w):
                if w[0][j] != words[index][j]:
                    dif += 1
                elif dif > 1:
                    break
            if dif == 1 :
                q.append((words.pop(index),w[1]+1))
                m += 1 
            i += 1
            index = i - m
    return answer
