def trans_t(t):
    t = t.split(":")
    return int(t[0])*60+int(t[1])

def retrans_t(t):
    t1 = str(t//60)
    t2 = str(t - (t//60)*60)
    if len(t1) == 1:
        t1 = "0"+t1
    if len(t2) == 1:
        t2 = "0"+t2
    return t1+":"+t2

def solution(n, t, m, timetable):
    answer = ''
    new_tt=[] 
    bus = trans_t("09:00")
    for tt in timetable:
        tt = trans_t(tt)
        new_tt.append(tt)
    new_tt.sort()
    
    for i in range(n):
        passengers=[]
        while new_tt:
            crow = new_tt[0]
            if crow <= bus and len(passengers) < m:
                passengers.append(new_tt.pop(0))
            else:
                break
        bus += t
        if i== n-1:
            if len(passengers)<m:
                answer = retrans_t(540 +(i)*t)
            else:
                answer = retrans_t(passengers[-1]-1)

    return answer
