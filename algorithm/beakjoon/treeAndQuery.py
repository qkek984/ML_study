import sys
sys.setrecursionlimit(10 ** 9)

N,R,Q = list(map(int,input().split()))
nodes = [[] for i in range(N+1)]
dp = [0]*(N+1)
visited = [False]*(N+1)
for i in range(N-1):
    a,b =map(int,sys.stdin.readline().split())
    nodes[a].append(b)
    nodes[b].append(a)

def dfs(n):
    result = 1
    for node in nodes[n]:
        if visited[node] == False:
            visited[node]=True
            result += dfs(node)
    dp[n] = result
    return result
visited[R] = True
dfs(R)

for i in range(Q):
    print(dp[int(sys.stdin.readline())])
