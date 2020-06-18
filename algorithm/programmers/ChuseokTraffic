def timeCalc(line):
    line = line.split()
    hms = list(map(float,line[1].split(":")))
    op_time = round(float(line[2][:-1])-0.001,3)
    endTime = (3600*24)+(hms[0]*3600)+(hms[1]*60)+hms[2]
    startTime= round(endTime-op_time,3)
    return startTime, endTime

def solution(lines):
    tp = []
    for line in lines:
        tp.append(timeCalc(line))
    maxValue = 0
    for t in tp:
        k=[0,0]
        for comp_t in tp:
            if not (comp_t[1] < t[0] or t[0]+1 <= comp_t[0]):
                k[0] += 1
            if not (comp_t[1] < t[1] or t[1]+1 <= comp_t[0]):
                k[1] += 1
        maxValue= max(maxValue,k[0],k[1])
    return maxValue
