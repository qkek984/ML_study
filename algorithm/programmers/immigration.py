def solution(n, times): 
    left = 0
    right = max(times)*n
    answer = 0
    while left <= right:
        mid = (left+right)//2
        t = 0
        for item in times:
            t += mid //item
            if t >= n:
                break
        if n <= t:
            answer = mid
            right = mid-1
        elif n >= t:
            left = mid+1
        
    return answer
