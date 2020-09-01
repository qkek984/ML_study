def solution(money):
    lenMoney = len(money)
    dp1 = [0] + [money[0]] + [0] * (lenMoney-2)
    for i in range(2,lenMoney-1):
        prepre = i-2
        pre = i-1
        idx = i+1
        dp1[idx] = max(dp1[prepre]+money[i], dp1[pre]+money[i])
    
    dp2 = [0,0] + [money[1]] + [0] * (lenMoney-2)
    for i in range(2,lenMoney):
        prepre = i-2
        pre = i-1
        idx = i+1
        dp2[idx] = max(dp2[prepre]+money[i], dp2[pre]+money[i])
        
    return max(dp1+dp2)
