def check(arr1, arr2):
    answer = 0
    len_arr1 = len(arr1)
    len_arr2 = len(arr2)
    if len_arr1 > len_arr2:
        arr1=arr1[len_arr1-len_arr2:]
    arr2 = list(arr2)
    arr2.reverse()
    arr2= ''.join(arr2)
    for i in range(len_arr2):
        this_answer = (len_arr2*2)-(i*2)
        if answer >= this_answer:
            break
        elif arr1[i:]==arr2[i:]:
            answer = this_answer
    return answer
    
def solution(s):
    answer = 1
    len_s = len(s)
    if len_s == 0:
        return 0
    for i in range(len_s):
        front = s[:i]
        rear = s[i:i*2]
        answer1 = check(front,rear)
        if i-1> 0:
            front = s[:i-1]
            rear = s[i:i*2-1]
            answer2 = check(front,rear) +1
        else:
            answer2 = 0
        answer=max(answer,answer1,answer2)
    return answer
