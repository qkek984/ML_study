n, m , h = map(int,input().split())
place = [[0 for _ in range(n+1)] for _ in range(h+1)]
node = [(-1,-1),(-1,-1),(-1,-1)]
for x in range(1,h+1):
    for y in range(1,n):
        node.append((x,y))

for _ in range(m):
    x,y = map(int,input().split())
    place[x][y] = 1
    node.pop(node.index((x,y)))
    if (x, y+1) in node:
        node.pop(node.index((x, y+1)))
    if (x,y-1) in node:
        node.pop(node.index((x, y-1)))


def check(add_node):
    for item in add_node:
        x, y = item
        if (x, y - 1) in add_node or (x, y+1) in add_node:
            return False
    return True

def down(add_node):
    for j in range(1,n+1):
        y = j
        for x in range(1,h+1):
            if place[x][y] == 1:
                y += 1
            elif place[x][y-1] == 1:
                y -= 1
            if (x,y) in add_node:
                y += 1
            elif (x,y-1) in add_node:
                y -= 1
        if j != y:
            return False
    return True

def result():
    for i in range(len(node)):
        for j in range(i+1,len(node)):
            for k in range(j + 1, len(node)):
                add_node={node[i]:1,node[j]:1,node[k]:1}
                if check(add_node)== False:
                    continue
                elif down(add_node):
                    answer = 3
                    if (-1,-1) in add_node:
                        answer = len(add_node)-1
                    return answer
    return -1

print(result())
