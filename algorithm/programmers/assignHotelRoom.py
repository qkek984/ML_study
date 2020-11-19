import sys
sys.setrecursionlimit(200001)
def findRoom(room,dic):
    if room not in dic:
        dic[room] = room+1
        return room
    else:
        result = findRoom(dic[room],dic)
        dic[room]=result+1
        return result
    
def solution(k, room_number):
    answer = []
    dic={}
    for room in room_number:
        num = findRoom(room,dic)
        answer.append(num)
    return answer
