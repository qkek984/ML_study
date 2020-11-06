N = int(input())
meeting = []
for _ in range(N):
    meeting.append(tuple(map(int,input().split())))
meeting.sort(key= lambda x:(x[0],x[1]))

answer = 1
allocated = meeting.pop(0)
for m in meeting:
    start, end = m
    if allocated[1] <= start:
        allocated = m
        answer += 1
    elif allocated[1] > end:
        allocated = m
print(answer)
