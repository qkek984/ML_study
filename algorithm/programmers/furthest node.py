from collections import deque
def solution(n, edge):
    dist = [-1 for i in range(n+1)]
    nodes = [[] for i in range(n+1)]
    for ed in edge:
        nodes[ed[0]].append(ed[1])
        nodes[ed[1]].append(ed[0])
    q = deque([1])
    dist[1] = 0
    while q:
        this = q.popleft()
        for node in nodes[this]:
            if dist[node] == -1:
                dist[node] = dist[this] + 1
                q.append(node)
    return dist.count(max(dist))
