def solution(dirs):
    answer = 0
    visited = set([])
    p=(5,5)
    dx,dy = (-1,1,0,0),(0,0,1,-1)
    command = {"U":0,"D":1,"R":2,"L":3}
    for d in dirs:
        mx = p[0] + dx[command[d]]
        my = p[1] + dy[command[d]]
        if (mx < 0 or 10 < mx) or (my < 0 or 10 < my):
            continue
        else:
            visited.add((p[0],p[1],mx,my))
            visited.add((mx,my,p[0],p[1]))
            p = (mx,my)
    answer=len(visited)/2
    return answer
