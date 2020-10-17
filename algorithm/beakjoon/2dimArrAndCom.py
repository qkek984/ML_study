r,c,k = map(int,input().split(" "))
array = []
for _ in range(3):
    array.append(list(map(int,input().split(" "))))
answer = -1
def myLenCol(array):
    maxValue = -1
    for arr in array:
        maxValue = max(len(arr),maxValue)
    return maxValue

def R(array):
    newArray = []
    maxRow = -1
    for arr in array:
        count = {}
        for a in arr:
            if a == 0:
                continue
            elif a in count:
                count[a] += 1
            else:
                count[a] = 1
        tmp=[]
        for c in count:
            tmp.append((c,count[c]))
        tmp = sorted(tmp, key=lambda k:(k[1],k[0]))
        newRow=[]
        for j in range(len(tmp)):
            if j == 50:
                break
            newRow.append(tmp[j][0])
            newRow.append(tmp[j][1])
        newArray.append(newRow)
        maxRow = max(maxRow,len(newRow))
    for i in range(len(newArray)):
        zero = maxRow - len(newArray[i])
        newArray[i] += [0]*zero
    return newArray

def C(array):
    newArr = []
    for i in range(len(array)):
        for j in range(len(array[i])):
            if i == 0:
                newArr.append([array[i][j]])
            else:
                newArr[j].append(array[i][j])
    return newArr

for i in range(0,101):
    lenRow = len(array)
    lenCol = len(array[0])
    if r-1<lenRow and c-1 < lenCol:
        if array[r-1][c-1] == k:
            answer = i
            break

    if lenRow >= lenCol:
        array =  R(array)
    else:
        array = C(R(C(array)))

print(answer)
