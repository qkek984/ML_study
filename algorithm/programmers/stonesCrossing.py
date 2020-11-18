def check(stones,k,mid):
    count = k
    for i in range(len(stones)):
        if stones[i] < mid:
            count -= 1
        else:
            count = k
        if count == 0:
            return False
    return True
        
def solution(stones, k):
    answer = 0
    left = 1
    right = max(stones)+1
    while left <= right:
        mid = (left + right) //2
        result = check(stones,k,mid)
        if result:
            left = mid+1
            answer = mid
        else:
            right = mid-1
    return answer
