def dfs(routes, tickets,lentickets):
    depart = routes[-1]
    result =[]
    for i in range(len(tickets)):
        if depart == tickets[i][0]:
            rest_tickets = tickets[:i] + tickets[i+1:]
            rou, res = dfs(routes+[tickets[i][1]], rest_tickets, lentickets)
            if lentickets == len(rou):
                result.append(rou)  
            elif res:
                for i in range(len(res)):
                    result.append(res[i])
    return routes, result

def solution(tickets):
    answer = []
    tickets.sort()
    lentickets = len(tickets)+1
    for i in range(len(tickets)):
        t1,t2 = tickets[i]
        if t1 == "ICN":
            routes = [t1,t2]
            rest_tickets = tickets[:i] + tickets[i+1:]
            _, result = dfs(routes, rest_tickets, lentickets)
            for i in range(len(result)):
                answer.append(result[i])
    return answer[0]
