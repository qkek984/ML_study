def solution(skill, skill_trees):
    answer = 0
    for st in skill_trees:
        s_list = list(skill)
        flag=True
        for word in st:
            if word in s_list:
                if word == s_list[0]:
                    s_list.pop(0)
                else:
                    flag=False
                    break
        if flag == True:
            answer += 1
    return answer
