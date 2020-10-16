from collections import deque
green = [[0,0,0,0] for _ in range(6)]
blue = [[0,0,0,0] for _ in range(6)]
score = 0
def move(tile, t, y, n):
    for i in range(2,6):
        if t == 1 or t == 3:
            if tile[i][y] != 0:
                if t == 1:
                    tile[i-1][y] = n
                    break
                elif t == 3:
                    tile[i - 1][y] = n
                    tile[i - 2][y] = n
                    break
        elif t == 2:
            if tile[i][y] != 0 or tile[i][y+1]:
                tile[i-1][y] = n
                tile[i-1][y+1] = n
                break
    else:
        if t == 1:
            tile[-1][y] = n
        elif t == 2:
            tile[-1][y] = n
            tile[-1][y+1] = n
        else:
            tile[-1][y] = n
            tile[-2][y] = n

def remove_check(tile):
    local_score = 0
    for i in range(2,6):
        if tile[i].count(0) == 0:
            local_score += 1
            tile[i] = [0, 0, 0, 0]
    return local_score

def down_block(tile):
    block = deque([])
    for i in range(4, 0, -1):
        for j in range(4):
            if tile[i][j] == 0:
                continue
            elif j+1 <4 and tile[i][j] == tile[i][j+1]:# t == 2
                block.append((2, j, tile[i][j]))
                tile[i][j] = 0
                tile[i][j+1] = 0
            elif tile[i][j] == tile[i-1][j]: #t == 3
                block.append((3, j, tile[i][j]))
                tile[i][j] = 0
                tile[i-1][j] = 0
            else:#t == 1
                block.append((1, j, tile[i][j]))
                tile[i][j] = 0
    return block

def special_block(tile):
    for i in range(2):
        if tile[i].count(0) != 4:
            tile.pop()
            tile.insert(0,[0,0,0,0])

N = int(input())
for n in range(1, N+1):
    t, x, y = map(int,input().split(" "))
    q= deque([(t,y,n)])
    while q:
        lt,ly,ln = q.popleft()
        move(green, lt,ly,ln)
        if not q:
            local_score = remove_check(green)
            if local_score > 0:
                score += local_score
                block = down_block(green)
                q += block
            special_block(green)

    if t == 2:
        bt=3
    elif t ==3:
        bt=2
    else:
        bt=t
    q= deque([(bt,x,n)])
    while q:
        lt,ly,ln = q.popleft()
        move(blue, lt,ly,ln)
        if not q:
            local_score = remove_check(blue)
            if local_score > 0:
                score += local_score
                block = down_block(blue)
                q += block
            special_block(blue)

tile_num = 0
for i in range(6):
    tile_num += (4 - green[i].count(0))
    tile_num += (4 - blue[i].count(0))

print(score)
print(tile_num)
