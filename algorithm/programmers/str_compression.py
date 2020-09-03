def solution(s):
    answer = [len(s)]
    N = (len(s)//2)+1

    for i in range(1,N):
        comp=[]
        count = 1
        for j in range(0, len(s), i):
            current_str = s[j:j+i]
            if not comp:
                comp.append(current_str)
            elif comp[-1] != current_str:
                if count > 1:
                    comp.insert(0,str(count))
                comp.append(current_str)
                count= 1
            elif comp[-1] == current_str:
                count += 1
        if count > 1:
            comp.insert(0,count)
        tmp = ''.join(map(str,comp))
        answer.append(len(tmp))
    return min(answer)
