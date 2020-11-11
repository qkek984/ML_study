from itertools import combinations
from collections import deque
def solution(user_id, banned_id):
    answer = 0
    len_ban_id = len(banned_id)
    banned_id.sort()
    ban_info=[]
    for i in range(len(banned_id)):
        if i>0 and banned_id[i] == banned_id[i-1]:
            ban_info[-1][2] += 1
            continue
        star=[]
        for j in range(len(banned_id[i])):
            if banned_id[i][j]=="*":
                star.append(j)
        ban_info.append([banned_id[i],star,1])

    case = [[] for _ in range(len(ban_info))]
    result = [set([])]
    for i in range(len(ban_info)):
        ban_id, star, select = ban_info[i]
        for u_id in user_id:
            if len(ban_id) != len(u_id):
                continue
            tmp_id = u_id
            for idx in star:
                tmp_id = tmp_id[:idx]+"*"+tmp_id[idx+1:]
            if tmp_id == ban_id:
                case[i].append(u_id)
        combs = combinations(case[i],select)
        new_result = []
        for comb in combs:
            comb = set(comb)
            for r in result:
                new_result.append(r.union(set(comb)))
        result = new_result
    result=deque(result)
    while result:
        r = result.popleft()
        if (len(r) == len_ban_id) and (not r in result):
             answer += 1
    return answer
