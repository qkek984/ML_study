def solution(people, limit):
    answer = 0
    people.sort(reverse=True)
    min_w = people[-1]
    for i in range(len(people)-1):
        if people[i] + min_w > limit:
            answer += 1
        else:
            people = people[i:]
            break
    else:
        people = people[-1:]
        
    max_w = people[0]
    weight = [0]*(max_w+1)
    for i in range(len(people)):
        weight[people[i]] += 1
    
    for i in range(len(people)):
        if weight[people[i]] == 0:
            continue
        else:
            weight[people[i]] -= 1
            max_idx = limit - people[i]
            max_idx = min(max_idx, max_w)
            for j in range(max_idx,39,-1):
                if weight[j] != 0:
                    if people[i] + j <= limit:
                        weight[j] -= 1
                        break
            answer += 1

    return answer
