def solution(s):
    answer = []
    s = s.split("}")
    new_s=[None for _ in range(len(s[:-2]))]
    for i in range(len(s[:-2])):
        tmp = list(map(int,s[i][2:].split(",")))
        new_s[len(tmp)-1] = tmp
    for i in range(len(new_s)):
        for j in range(len(new_s[i])):
            if not new_s[i][j] in answer:
                answer.append(new_s[i][j])
    return answer
