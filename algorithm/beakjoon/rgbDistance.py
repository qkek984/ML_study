N= int(input())
cost = [0,0,0]
for _ in range(N):
    rgb = list(map(int,input().split()))
    tmpCost=[[],[],[]]
    for i in range(3):#cost
        for j in range(3):#rgb
            if i != j:
                tmpCost[j].append(cost[i]+rgb[j])
    cost = [min(tmpCost[0]),min(tmpCost[1]),min(tmpCost[2])]
print(min(cost))
