import itertools
N , M = map(int,input().split())
array=[]
for i in range(0,N):
    array.append(list(map(int,input().split())))
house=[]
chicken=[]

for i in range(0,N):
    for j in range(0,N):
        if array[i][j]==1:
            house.append((i,j))
        elif array[i][j]==2:
            chicken.append((i,j))

item = [i for i in range(len(chicken))] # 0 1 2 3
comb = list(itertools.combinations(item,M))
dist=None
for i in range(0,len(comb)):
    thisCombDist=0
    for j in range(0,len(house)):
        minDist=None
        for k in range(0,len(comb[0])):
            index=comb[i][k]
            thisDist = abs(chicken[index][0]-house[j][0])+abs(chicken[index][1]-house[j][1])
            if minDist== None or minDist>thisDist:
                minDist=thisDist
        thisCombDist += minDist
    if dist ==None or dist >thisCombDist:
        dist = thisCombDist
print(dist)
