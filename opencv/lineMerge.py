import cv2
import math
import numpy as np

def get_lines(lines_in):
    if cv2.__version__ < '3.0':
        return lines_in[0]
    return [l[0] for l in lines_in]

def process_lines(image_src):
    img = cv2.imread(image_src)
    #cv2.imshow('orginal',img)
    height,width = img.shape[:2]

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #cv2.imshow("gray",gray)

    edges = cv2.Canny(gray, threshold1=50, threshold2=150, apertureSize = 3)
    #cv2.imshow("Canny", edges)
    lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/180, threshold=50,
                            minLineLength=50, maxLineGap=30)


    # l[0] - line; l[1] - angle
    for line in get_lines(lines):
        leftx, boty, rightx, topy = line
        cv2.line(img, (leftx, boty), (rightx,topy), (0,0,255), 1)
    #cv2.imshow("lines", img)

    # merge lines

    #------------------
    # prepare
    _lines = []
    for _line in get_lines(lines):
        _lines.append([(_line[0], _line[1]),(_line[2], _line[3])])

    # sort
    _lines_x = []
    _lines_y = []
    for line_i in _lines:
        orientation_i = math.atan2((line_i[0][1]-line_i[1][1]),(line_i[0][0]-line_i[1][0]))
        if (abs(math.degrees(orientation_i)) > 45) and abs(math.degrees(orientation_i)) < (90+45):
            _lines_y.append(line_i)
        else:
            _lines_x.append(line_i)

    _lines_x = sorted(_lines_x, key=lambda _line: _line[0][0])
    _lines_y = sorted(_lines_y, key=lambda _line: _line[0][1])

    merged_lines_x = merge_lines_pipeline_2(_lines_x)
    merged_lines_y = merge_lines_pipeline_2(_lines_y)

    merged_lines_all = []
    merged_lines_all.extend(merged_lines_x)
    merged_lines_all.extend(merged_lines_y)
    print("process groups lines", len(_lines), len(merged_lines_all))

    # ----------find gradient

    print("------------------------4-------------")
    merged_lines_all=np.reshape(merged_lines_all,(-1,4))
    print("-------------------------------------")

    img_merged_lines = cv2.imread(image_src)

    colLines=limitGradient(merged_lines_all,95,85)
    rowLines=limitGradient(merged_lines_all,185,175)
    cols=[[[0,0,0,height]]]
    rows=[[[0,0,width,0]]]
    for i, line in enumerate(rowLines):
        #print line
        avg = (line[0][1] + line[0][3]) / 2
        line = [[ line[0][0],avg, line[0][2], avg ]]
        rows.append([[ line[0][0],avg, line[0][2], avg ]])
        #cv2.line(img_merged_lines, (line[0][0], line[0][1]), (line[0][2], line[0][3]), (0, 0, 255), 2)
    rows.append([[0,height,width,height]])
    for i, line in enumerate(colLines):
        #print line
        avg = (line[0][0] + line[0][2]) / 2
        line = [[ avg, line[0][1], avg, line[0][3] ]]
        cols.append([[ avg, line[0][1], avg, line[0][3] ]])
        cv2.line(img_merged_lines, (line[0][0], line[0][1]), (line[0][2], line[0][3]), (255, 50, 50), 8)
        cv2.putText(img_merged_lines, "col", (line[0][0], line[0][1]+30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
    cols.append([[width,0,width,height]])
     ##############
    print rows
    inp = mappingP(500,False,height)
    print ("in",inp)
    pad=15
    f1 = open("test.html", "w")
    f2 = open("test.css", "w")
    css=""
    text = "<html>\n"
    text += "<head><link rel=stylesheet type=text/css href=test.css></head>\n"
    text += "<body>\n"
    divI=0
    for index, row in enumerate(rows[0:len(rows)]):

        flag=True
        if index<len(rows)-1:
            i = index+1
        else:
            flag= False
        while(abs(row[0][0]-rows[i][0][0])>30 and abs(row[0][2]-rows[i][0][2])>30):
            if i < len(rows) - 1:
                i = i + 1
            else:
                flag = False
                break
        '''
        tx1=row[0][0]
        ty1=row[0][1]
        tx2=row[0][2]
        ty2=row[0][3]
        bx1 = rows[i][0][0]
        by1 = rows[i][0][1]
        bx2 = rows[i][0][2]
        by2 = rows[i][0][3]
        '''
        if flag==True:
            if i>1:
                cv2.line(img_merged_lines, (row[0][0], row[0][1]), (row[0][2], row[0][3]), (255, 50, 50), 8)
                cv2.putText(img_merged_lines,"row",(row[0][0], row[0][1]-20),cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,0,0),2)
            if row[0][0]<25 and rows[i][0][0]<25:
                row[0][0]=rows[i][0][0]=0
            if width-row[0][2]<25 and width-rows[i][0][2]<25:
                row[0][2] = rows[i][0][2] = width
            print ("iteration", i)
            print ("row", row)
            print ("rows", rows[i])
            # if rows[i][0]
            tmpcol=[]
            for col in cols[1:len(cols)-1]:
                print ("col", col)
                if (row[0][0]<col[0][0]-pad and col[0][0]-pad<row[0][2]):#in high row
                    if (row[0][1] <= col[0][1]+pad) and (rows[i][0][1]>(col[0][3]-pad)):
                        print("suc2")
                        tmpcol.append(col)

            if len(tmpcol)==0:
                print('rect: ',row[0][0],row[0][1],"and",rows[i][0][2],rows[i][0][3])
                text += "<div id=div"+str(divI)+">"+str(divI)+"</div>\n"
                css += divCss(divI, mappingP(rows[i][0][2],width,False), mappingP(rows[i][0][3]-row[0][1],False,height),None)
                divI += 1
            else:
                print('rectd: ', row[0][0], row[0][1], "and", rows[i][0][2], rows[i][0][3])
                text += "<div id=div" + str(divI) + ">\n"
                css += divCss(divI, mappingP(rows[i][0][2], width, False),
                              mappingP(rows[i][0][3] - row[0][1], False, height),None)
                divI += 1
                for j, mcol in enumerate(tmpcol):
                    if j==0:
                        print("??")
                        #print('rect: ', row[0][0], row[0][1], "and", tmpcol[j][0][2], tmpcol[j][0][3])
                        print('rect: ', row[0][0], row[0][1], "and", tmpcol[j][0][2], rows[i][0][3])
                        text += "\t<div id=div" + str(divI) + ">" + str(divI) + "</div>\n"
                        css += divCss(divI, mappingP(tmpcol[j][0][2], width, False),
                                      100,"float:left;\n\t")
                        divI += 1
                    if j!=0:
                        print("????????????????????")
                        print('rect: ', tmpcol[j-1][0][0], row[0][1], "and", tmpcol[j][0][2], tmpcol[j][0][3])
                        text += "\t<div id=div" + str(divI) + ">" + str(divI) + "</div>\n"
                        css += divCss(divI, mappingP(tmpcol[j][0][2]-tmpcol[j-1][0][0], width, False),
                                      100,"float:left;\n\t")
                        divI += 1
                    if j==len(tmpcol)-1:
                        #print('rect: ', tmpcol[j][0][0], tmpcol[j][0][1], "and", rows[j][0][2], rows[j][0][3])
                        print('rect: ', tmpcol[j][0][0], row[0][1], "and", rows[i][0][2], rows[i][0][3])
                        text += "\t<div id=div" + str(divI) + ">" + str(divI) + "</div>\n"
                        css += divCss(divI, mappingP(rows[i][0][2]-tmpcol[j][0][2], width, False),
                                      100,"float:left;\n\tborder:0;\n\t")
                        divI += 1
                    print (j,"jj",len(tmpcol)-1)

                text += "</div>\n"

        print("------------------------")
    text += "\n</body>\n</html>"
    f1.write(text)
    f1.close()

    f2.write(css)
    f2.close()
    cv2.imshow("result",img_merged_lines)
    return merged_lines_all

def mappingP(p,width,height):
    if width != False:
        return int(float(p)/float(width)*100)
    elif height != False:
        return int(float(p)/float(height)*100)

def divCss(id,width,height,plus):
    div="#div"+str(id)+"{\n\tborder:0.1px solid blue;\n\t"
    div += "width:"+str(width)+"%;\n\t"
    print ("w:",width)
    div += "height:" + str(height) + "%;\n\t"
    if plus != None:
        div += plus
    div+="}"
    return div


def limitGradient(lines,maxG,minG):
    # row-----------------------------------------------------------------------------------------
    slope_degree = (np.arctan2(lines[:, 1] - lines[:, 3], lines[:, 0] - lines[:, 2]) * 180) / np.pi
    # limit 1
    lines = lines[np.abs(slope_degree) < maxG]
    slope_degree = slope_degree[np.abs(slope_degree) < maxG]
    # limit 2
    lines = lines[np.abs(slope_degree) > minG]
    slope_degree = slope_degree[np.abs(slope_degree) > minG]

    lines = lines[(abs(slope_degree) > 0), :]

    lines = lines[:, None]
    return lines

def merge_lines_pipeline_2(lines):
    super_lines_final = []
    super_lines = []
    min_distance_to_merge = 30
    min_angle_to_merge = 30

    for line in lines:
        create_new_group = True
        group_updated = False

        for group in super_lines:
            for line2 in group:
                if get_distance(line2, line) < min_distance_to_merge:
                    # check the angle between lines
                    orientation_i = math.atan2((line[0][1]-line[1][1]),(line[0][0]-line[1][0]))
                    orientation_j = math.atan2((line2[0][1]-line2[1][1]),(line2[0][0]-line2[1][0]))

                    if int(abs(abs(math.degrees(orientation_i)) - abs(math.degrees(orientation_j)))) < min_angle_to_merge:
                        #print("angles", orientation_i, orientation_j)
                        #print(int(abs(orientation_i - orientation_j)))
                        group.append(line)

                        create_new_group = False
                        group_updated = True
                        break

            if group_updated:
                break

        if (create_new_group):
            new_group = []
            new_group.append(line)

            for idx, line2 in enumerate(lines):
                # check the distance between lines
                if get_distance(line2, line) < min_distance_to_merge:
                    # check the angle between lines
                    orientation_i = math.atan2((line[0][1]-line[1][1]),(line[0][0]-line[1][0]))
                    orientation_j = math.atan2((line2[0][1]-line2[1][1]),(line2[0][0]-line2[1][0]))

                    if int(abs(abs(math.degrees(orientation_i)) - abs(math.degrees(orientation_j)))) < min_angle_to_merge:
                        #print("angles", orientation_i, orientation_j)
                        #print(int(abs(orientation_i - orientation_j)))

                        new_group.append(line2)

                        # remove line from lines list
                        #lines[idx] = False
            # append new group
            super_lines.append(new_group)


    for group in super_lines:
        super_lines_final.append(merge_lines_segments1(group))

    return super_lines_final

def merge_lines_segments1(lines, use_log=False):
    if(len(lines) == 1):
        return lines[0]

    line_i = lines[0]

    # orientation
    orientation_i = math.atan2((line_i[0][1]-line_i[1][1]),(line_i[0][0]-line_i[1][0]))

    points = []
    for line in lines:
        points.append(line[0])
        points.append(line[1])

    if (abs(math.degrees(orientation_i)) > 45) and abs(math.degrees(orientation_i)) < (90+45):

        #sort by y
        points = sorted(points, key=lambda point: point[1])

        if use_log:
            print("use y")
    else:

        #sort by x
        points = sorted(points, key=lambda point: point[0])

        if use_log:
            print("use x")

    return [points[0], points[len(points)-1]]


def lineMagnitude (x1, y1, x2, y2):
    lineMagnitude = math.sqrt(math.pow((x2 - x1), 2)+ math.pow((y2 - y1), 2))
    return lineMagnitude


def DistancePointLine(px, py, x1, y1, x2, y2):
    LineMag = lineMagnitude(x1, y1, x2, y2)

    if LineMag < 0.00000001:
        DistancePointLine = 9999
        return DistancePointLine

    u1 = (((px - x1) * (x2 - x1)) + ((py - y1) * (y2 - y1)))
    u = u1 / (LineMag * LineMag)

    if (u < 0.00001) or (u > 1):
        #// closest point does not fall within the line segment, take the shorter distance
        #// to an endpoint
        ix = lineMagnitude(px, py, x1, y1)
        iy = lineMagnitude(px, py, x2, y2)
        if ix > iy:
            DistancePointLine = iy
        else:
            DistancePointLine = ix
    else:
        # Intersecting point is on the line, use the formula
        ix = x1 + u * (x2 - x1)
        iy = y1 + u * (y2 - y1)
        DistancePointLine = lineMagnitude(px, py, ix, iy)

    return DistancePointLine

def get_distance(line1, line2):
    dist1 = DistancePointLine(line1[0][0], line1[0][1],
                              line2[0][0], line2[0][1], line2[1][0], line2[1][1])
    dist2 = DistancePointLine(line1[1][0], line1[1][1],
                              line2[0][0], line2[0][1], line2[1][0], line2[1][1])
    dist3 = DistancePointLine(line2[0][0], line2[0][1],
                              line1[0][0], line1[0][1], line1[1][0], line1[1][1])
    dist4 = DistancePointLine(line2[1][0], line2[1][1],
                              line1[0][0], line1[0][1], line1[1][0], line1[1][1])
    return min(dist1,dist2,dist3,dist4)

'''-------------------------main------------------------'''

process_lines('c5.jpg')

cv2.waitKey(0)
cv2.destroyAllWindows()