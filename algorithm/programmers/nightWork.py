import heapq
def solution(n, works):
    answer = 0
    heap=[]
    for w in works:
        heapq.heappush(heap,-w)
    for i in range(n):
        if heap:
            w = heapq.heappop(heap)
        else:
            break
        if w+1 != 0:
            heapq.heappush(heap,w+1)
    for w in heap:
        answer += w*w
    return answer
