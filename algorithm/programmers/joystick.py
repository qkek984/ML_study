from collections import deque
def change(item,idx,alpha):
    target = alpha.index(item)
    return min(target, 26-target)

def find(len_name, n, name, idx):
    left = -1
    l_count = 0
    right = -1
    r_count = 0
    for i in range(1,len_name):
        l_count += 1
        i = (idx-i)%len_name
        if n[i] != name[i]:
            left = i
            break
    for i in range(1,len_name):
        r_count += 1
        i = (i+idx)%len_name
        if n[i] != name[i]:
            right = i
            break

    return left,l_count,right,r_count
def solution(name):
    answer = 987654321
    alpha=['A','B','C','D','E','F','G','H','I','J',
           'K','L','M','N','O','P','Q','R','S','T',
           'U','V','W','X','Y','Z']
    len_name = len(name)
    init_name = ['A' for _ in range(len(name))]
    q = deque([(list(init_name),0,0)])
    i_c = 0
    while q:
        n, idx, count = q.popleft()
        count += change(name[idx],idx, alpha)
        n[idx] = name[idx]

        left,l_count,right,r_count = find(len_name, n,name,idx)
        if left == -1:
            answer = min(answer, count)
        else:
            q.append((n.copy(), left, count+l_count))

        if right == -1:
            answer = min(answer, count)
        else:
            q.append((n.copy(), right, count+r_count))
    return answer
