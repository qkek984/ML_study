def solution(N, number):
    if N == number:
        return 1
    
    answer = -1
    values=[0,{N}]
    
    for i in range(2,9):
        tmp={int(str(N)*(i))}
        half = int(i/2)
        
        for x_i in range(1,half+1):
            y_i = i-x_i
            for x in values[x_i]:
                for y in values[y_i]:
                    tmp.add(x+y)
                    tmp.add(x-y)
                    tmp.add(y-x)
                    tmp.add(x*y)
                    if y != 0:
                        tmp.add(x//y)
                    if x != 0:
                        tmp.add(y//x)
        if number in tmp:
            answer = i
            break
        else:
            values.append(tmp)
            
    return answer
