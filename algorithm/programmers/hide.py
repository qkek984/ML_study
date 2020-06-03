def solution(clothes):
    answer = 1
    print(clothes)
    clothes = sorted(clothes, key=lambda clothes: clothes[1])
    tmp=""
    cCount=[]
    for c in clothes:
        if tmp != c[1]:
            tmp = c[1]
            cCount.append([[c[1],1]])
        else:
            cCount[-1][0][1] += 1 

    for co in cCount:
        answer *= co[0][1]+1
    answer -= 1

    return answer
