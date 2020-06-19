def solution(n):
    answer = []
    for i in range(0,n):
        tmp=[]
        for i in range(len(answer)-1,-1,-1):
            if answer[i] == 0:
                tmp.append(1)
            else: 
                tmp.append(0)     
        answer = answer + [0]+ tmp
    return answer
