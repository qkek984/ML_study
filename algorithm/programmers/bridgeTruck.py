def solution(bridge_length, weight, truck_weights):
    answer = 1
    passed=[]
    ing=[]
    ingTime=[]
    while(True):
        popCount=0
        for i in range(0,len(ingTime)):
            if ingTime[i-popCount] == bridge_length-1:
                passed.append(ing[0])
                ing.pop(0)
                ingTime.pop(0)
                
                popCount += 1
            else:
                ingTime[i-popCount] += 1

        if len(truck_weights)==0 and len(ing)==0:
            break
        elif len(truck_weights) != 0:
            if sum(ing) ==0:
                ing.append(truck_weights[0])
                ingTime.append(0)
                truck_weights.pop(0)
            elif (sum(ing)+truck_weights[0]) <= weight:
                ing.append(truck_weights[0])
                ingTime.append(0)
                truck_weights.pop(0)
        answer += 1
    return answer
