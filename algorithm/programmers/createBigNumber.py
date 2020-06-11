def solution(number, k):
    answer=[number[0]]
    for i in range(1,len(number)):
        while (len(answer) > 0) and (answer[-1] <number[i]) and (k>0):
            answer.pop()
            k -= 1
        answer.append(number[i])
    if k != 0:
        answer = answer[:-k]
    return ''.join(answer)
