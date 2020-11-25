def solution(gems):
    answer = [1,100001]
    size = len(set(gems))
    start,end = 0,0
    dic={gems[0]:1}
    while start < len(gems) and end<len(gems):
        if len(dic) == size:
            if (answer[1]-answer[0])>(end-start):
                answer = [start+1,end+1]
                
            dic[gems[start]] -=1
            if dic[gems[start]]==0:
                del dic[gems[start]]
            start += 1
        else:
            end += 1
            if end == len(gems):
                break
            if gems[end] not in dic:
                dic[gems[end]] = 1
            else:
                dic[gems[end]] += 1            

    return answer
