def solution(triangle):
    answer = 0
    values =[(triangle[0][0],0)]

    for i in range(1,len(triangle)):
        tmp=[]
        for j in range(0,len(values)):
            index = values[j][1]
            if j > 0:
                if tmp[-1][0] < values[j][0]+triangle[i][index]:
                    tmp[-1] = (values[j][0]+triangle[i][index],index)
            else:
                tmp.append((values[j][0]+triangle[i][index], index))
            tmp.append((values[j][0]+triangle[i][index+1], index+1))
        values = tmp
    answer = sorted(values,reverse=True)[0][0]
    return answer
