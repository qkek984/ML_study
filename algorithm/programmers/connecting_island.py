def solution(n, costs):
    answer = 0
    costs = sorted(costs, key= lambda x:x[2])
    visited = [0]*n
    visited[0] = 1
    while sum(visited) != n:
        for n1,n2,c in costs:
            if visited[n1] or visited[n2]:
                if visited[n1] and visited[n2]:
                    continue
                else:
                    visited[n1]=1
                    visited[n2]=1
                    answer += c
                    break
    return answer
