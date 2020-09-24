
def solution(n):
    dic = {0:1}
    answer = 0
    for i in range(0,n):
        tmp={}
        min_v=987654321
        for key in dic:
            a = key + 1
            b = key + 2
            min_v = min(min_v,b)
            if a >= n:
                if a ==n:
                    answer += dic[key]
            elif a in tmp:
                tmp[a] += dic[key]
            else:
                tmp[a] = dic[key]
            
            if b >= n:
                if b == n:
                    answer += dic[key]
            elif b in tmp:
                tmp[b] += dic[key]
            else:
                tmp[b] = dic[key]
        if min_v > 2000:
            break
        else:
            dic = tmp
    return answer%1234567
