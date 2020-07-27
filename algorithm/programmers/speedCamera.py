def solution(routes):
    answer = 1
    routes = sorted(routes)
    fr = [-30000 , 30000]
    for route in routes:
        front = route[0]
        rear =  route[1]
        if fr[0] <= front and rear <= fr[1]:
            fr = [front,rear]
        elif (fr[0] <= front and front <= fr[1]) and fr[1] <= rear:
            fr[0] = front
        else:
            fr=[front,rear]
            answer += 1
    return answer
