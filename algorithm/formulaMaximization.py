from itertools import permutations
def solution(expression):
    answer = 0
    exp = []
    tmp=""
    for e in expression:
        if e in ["+","-","*"]:
            exp.append(int(tmp))
            exp.append(e)
            tmp=""
        else:
            tmp += e
    exp.append(int(tmp))
    permutation = list(permutations(["+","-","*"],3))
    for per in permutation:
        arr = exp.copy()
        for p in per:
            new_arr = []
            while arr:
                this = arr.pop(0)
                if this == p:
                    if p == "+":
                        new_arr[-1] = new_arr[-1] + arr.pop(0)
                    elif p == "-":
                        new_arr[-1] = new_arr[-1] - arr.pop(0)
                    else:
                        new_arr[-1] = new_arr[-1] * arr.pop(0)
                else:
                    new_arr.append(this)
            arr = new_arr
        answer = max(answer,abs(arr[0]))
    return answer
