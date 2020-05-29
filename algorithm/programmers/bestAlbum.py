def solution(genres, plays):
    answer = []
    dicOrdi={}
    dicArray={}
    for i in range(0,len(plays)):
        if genres[i] in dicOrdi.keys():
            dicOrdi[genres[i]] += plays[i]
            dicArray[genres[i]].append((plays[i],i))
        else:
            dicOrdi[genres[i]] = plays[i]
            dicArray[genres[i]]=[(plays[i],i)]
    dicOrdi = sorted(dicOrdi.items(), key=lambda x:x[1], reverse=True)
    for key in dicOrdi:
        tmp = sorted(dicArray[key[0]], key=lambda x:(-x[0],x[1]))# 0번 인덱스 역순정렬 후 1번인덱스 순차정렬
        for i in range(0,len(dicArray[key[0]])):
            answer.append(tmp[i][1])
            if i ==1:
                break
    return answer
