def solution(a):
    answer = set([a[0],a[-1]])
    len_a=len(a)
    min_left = a[0]
    min_right = a[-1]

    for i in range(1,len(a)-1):
        if min_left > a[i]:
            answer.add(a[i])
        min_left = min(min_left,a[i])

        j = len_a-1-i
        if min_right > a[j]:
            answer.add(a[j])
        min_right = min(min_right,a[j])
    return len(answer)
