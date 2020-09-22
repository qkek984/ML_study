def solution(operations):
    q = []
    for op in operations:
        op=op.split(" ")
        if op[0]=='I':
            q.append(int(op[1]))
        elif q and op[0]=='D' and op[1]=='1':
            q.pop(q.index(max(q)))
        elif q:
            q.pop(q.index(min(q)))
    if q:
        answer=[max(q),min(q)]
    else:
        answer = [0,0]
    return answer
