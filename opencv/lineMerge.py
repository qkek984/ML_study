import cv2
import math
import numpy as np
import random
import collections

class LineMerge:
    def get_lines(self,lines_in):
        if cv2.__version__ < '3.0':
            return lines_in[0]
        return [l[0] for l in lines_in]

    def merge_lines_pipeline_2(self,lines):
        super_lines_final = []
        super_lines = []
        min_distance_to_merge = 30
        min_angle_to_merge = 30

        for line in lines:
            create_new_group = True
            group_updated = False

            for group in super_lines:
                for line2 in group:
                    if self.get_distance(line2, line) < min_distance_to_merge:
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
                    if self.get_distance(line2, line) < min_distance_to_merge:
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
            super_lines_final.append(self.merge_lines_segments1(group))

        return super_lines_final

    def merge_lines_segments1(self,lines, use_log=False):
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


    def lineMagnitude (self,x1, y1, x2, y2):
        lineMagnitude = math.sqrt(math.pow((x2 - x1), 2)+ math.pow((y2 - y1), 2))
        return lineMagnitude

    def DistancePointLine(self,px, py, x1, y1, x2, y2):
        LineMag = self.lineMagnitude(x1, y1, x2, y2)

        if LineMag < 0.00000001:
            DistancePointLine = 9999
            return DistancePointLine

        u1 = (((px - x1) * (x2 - x1)) + ((py - y1) * (y2 - y1)))
        u = u1 / (LineMag * LineMag)

        if (u < 0.00001) or (u > 1):
            #// closest point does not fall within the line segment, take the shorter distance
            #// to an endpoint
            ix = self.lineMagnitude(px, py, x1, y1)
            iy = self.lineMagnitude(px, py, x2, y2)
            if ix > iy:
                DistancePointLine = iy
            else:
                DistancePointLine = ix
        else:
            # Intersecting point is on the line, use the formula
            ix = x1 + u * (x2 - x1)
            iy = y1 + u * (y2 - y1)
            DistancePointLine = self.lineMagnitude(px, py, ix, iy)

        return DistancePointLine

    def get_distance(self,line1, line2):
        dist1 = self.DistancePointLine(line1[0][0], line1[0][1],
                                  line2[0][0], line2[0][1], line2[1][0], line2[1][1])
        dist2 = self.DistancePointLine(line1[1][0], line1[1][1],
                                  line2[0][0], line2[0][1], line2[1][0], line2[1][1])
        dist3 = self.DistancePointLine(line2[0][0], line2[0][1],
                                  line1[0][0], line1[0][1], line1[1][0], line1[1][1])
        dist4 = self.DistancePointLine(line2[1][0], line2[1][1],
                                  line1[0][0], line1[0][1], line1[1][0], line1[1][1])
        return min(dist1,dist2,dist3,dist4)

    def mergeLine(self,img,lines):
        # l[0] - line; l[1] - angle
        for line in self.get_lines(lines):
            leftx, boty, rightx, topy = line
            cv2.line(img, (leftx, boty), (rightx, topy), (0, 0, 255), 1)
        # cv2.imshow("lines", img)
        # -------------prepare
        _lines = []
        for _line in self.get_lines(lines):
            _lines.append([(_line[0], _line[1]), (_line[2], _line[3])])
        # ------------sort
        _lines_x = []
        _lines_y = []
        for line_i in _lines:
            orientation_i = math.atan2((line_i[0][1] - line_i[1][1]), (line_i[0][0] - line_i[1][0]))
            if (abs(math.degrees(orientation_i)) > 45) and abs(math.degrees(orientation_i)) < (90 + 45):
                _lines_y.append(line_i)
            else:
                _lines_x.append(line_i)

        _lines_x = sorted(_lines_x, key=lambda _line: _line[0][0])
        _lines_y = sorted(_lines_y, key=lambda _line: _line[0][1])

        _lines_x = sorted(_lines_x, key=lambda _line: _line[0][1])
        _lines_y = sorted(_lines_y, key=lambda _line: _line[0][0])

        # -------------merge lines
        merged_lines_x = self.merge_lines_pipeline_2(_lines_x)
        merged_lines_y = self.merge_lines_pipeline_2(_lines_y)

        merged_lines_all = []
        merged_lines_all.extend(merged_lines_x)
        merged_lines_all.extend(merged_lines_y)
        print("process groups lines", len(_lines), len(merged_lines_all))
        print("==========================================================================")
        merged_lines_all = np.reshape(merged_lines_all, (-1, 4))
        return merged_lines_all

class GetLine:
    def limitGradient(self,lines,maxG,minG):
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
    def avgMapping(self, lines, flag,img):
        height, width = img.shape[:2]
        #flag 1:row, 0:col
        if flag == 0:
            rows=[]
            for i, line in enumerate(lines):
                # print line
                avg = (line[0][1] + line[0][3]) / 2
                rows.append([[line[0][0], avg, line[0][2], avg]])
                # cv2.line(img_merged_lines, (line[0][0], line[0][1]), (line[0][2], line[0][3]), (0, 0, 255), 2)
            return rows
        else:
            cols=[]
            for i, line in enumerate(lines):
                # print line
                avg = (line[0][0] + line[0][2]) / 2
                cols.append([[avg, line[0][1], avg, line[0][3]]])
            return cols

class Html:
    def __init__(self,img):
        height, width = img.shape[:2]
        self.threshold = int(((height+width)/2)*0.03)
        #self.threshold=30
        print(self.threshold)
        self.text = None
        self.css = None
        self.f=[]
        self.divNum=0
        self.divList=[]
        self.rectList=[]
        self.divCssList=[]
    def startHtml(self, html, css):#input file Name > html, css
        if html !=None:
            self.f.append(open(html+".html", "w"))
            self.text = "<html>\n"
        if css != None:
            self.f.append(open(css+".css", "w"))
            self.text += "<head><link rel=stylesheet type=text/css href="+css+".css></head>\n"
            self.css=""
        self.text += "<body>\n"

    def putHtml(self,text):
        self.text += text

    def putCss(self,css):
        self.css += css

    def upDivNum(self,num):
        self.divNum+=num

    def endHtml(self):
        self.text += "\n</body>\n</html>"
        if self.text != None:
            self.f[0].write(self.text)
            self.f[0].close()
        if self.css != None:
            self.f[len(self.f)-1].write(self.css)
            self.f[len(self.f)-1].close()

    def mappingP(self, p,width,height):
        if width != False:
            return (float(p) / float(width) * 100)
        elif height != False:
            return (float(p) / float(height) * 100)

    def addDivList(self,id, width, height, etc):
        div = collections.OrderedDict()
        div['id'] = id
        div['width'] = str(width)+"%"
        div['height'] = str(height)+"%"
        div['dispaly'] = "table"
        div['border-collapse'] = "collapse"
        if etc != None:
            for dict in etc:
                for k, v in dict.items():
                    div[k] = v
        self.divCssList.append(div)

    def makeCssItem(self,css):
        text = str(css['id']) + "{\n"
        for k, v in css.items():
            if k != "id" and k != "class":
                text += "\t" + str(k) + " : " + str(v) + ";\n"
        text += "}\n"
        return text

    def preventOverlap(self,rect):
        for rectL in self.rectList:
            if rect==rectL:
                return False

        self.rectList.append(rect)
        print("rect:",rect)
        return True

    def makeCols(self, html,madeRows, cols, img, insertL, appendL):
        th=self.threshold
        inCols=[]
        fieldSet="<fieldset style=height:82%>"
        width,height= (insertL[0][2]-insertL[0][0]),(appendL[0][3]-insertL[0][3])
        for i, row in enumerate(madeRows):
            rectx1, recty1, rectx2, recty2 = row[0][0], row[0][1], row[0][2], row[0][3]
            rowGaps = row[1]
            colGaps = []
            for col in cols:
                x1,y1,x2,y2 = col[0][0],col[0][1],col[0][2],col[0][3]
                if (abs(recty1 - y1)<th and abs(recty2-y2)<th)and (rectx1-th<x1 and x1 < rectx2+th):
                    inCols.append([[x1,recty1,x2,recty2]])
                elif (y1<recty1 and recty2 < y2) or\
                        (abs(y1-recty1)<th and recty2 < y2)or\
                        (y1<recty1 and abs(recty2 - y2)<th):
                    inCols.append([[x1, recty1, x2, recty2]])
                    pass
                elif recty1-th<y1 and y2<recty2+th:
                    colGaps.append([[x1,y1,x2,y2]])

            if len(inCols)==0:
                if(self.preventOverlap([[rectx1,recty1,rectx2,recty2]])==True):
                    cv2.line(img, (int(rectx1), int(recty1)), (int(rectx2), int(recty1)), (255, 50, 50), 8)
                    cv2.line(img, (int(rectx1), int(recty2)), (int(rectx2), int(recty2)), (255, 50, 50), 8)
                    cv2.putText(img, "div"+str(self.divNum), (int(rectx1)+10,int(recty1)+20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                 (255, 0, 0), 2)

                    html.putHtml("<div id=div" + str(self.divNum) + ">"+fieldSet+str(self.divNum)+"</fieldset></div>\n")
                    html.addDivList(id="#div"+str(self.divNum), width=html.mappingP(rectx2-rectx1, width, False),
                                    height=html.mappingP(recty2-recty1, False, height), etc=None)
                    print("div" + str(self.divNum))
                    self.divList.append([["div" + str(self.divNum)],[rectx1,recty1,rectx2,recty2]])
                    html.upDivNum(+1)
            else:
                flag=False
                if(self.preventOverlap([[rectx1, recty1, rectx2, recty2]])):
                    cv2.line(img, (int(rectx1), int(recty2)), (int(rectx2), int(recty2)), (255, 50, 50), 8)
                    cv2.line(img, (int(rectx1), int(recty2)), (int(rectx2), int(recty2)), (255, 50, 50), 8)
                    html.putHtml("<div id=div" + str(self.divNum) + ">\n")
                    html.addDivList(id="#div" + str(self.divNum), width=html.mappingP(rectx2 - rectx1, width, False),
                                    height=html.mappingP(recty2 - recty1, False, height), etc=[{"border":"0px"}])
                    html.upDivNum(+1)
                    flag=True

                inCols.insert(0, [[rectx1,recty1,rectx1,recty2]])
                inCols.append([[rectx2,recty1,rectx2,recty2]])
                inCols = np.squeeze(inCols)

                for j,_ in enumerate(inCols[:-1]):
                    lx1, ly1, lx2, ly2 = inCols[j][0], inCols[j][1], inCols[j][2], inCols[j][3]
                    rx1, ry1, rx2, ry2 = inCols[j + 1][0], inCols[j + 1][1], inCols[j + 1][2], inCols[j + 1][3]
                    if rowGaps != []:
                        flag2=False
                        if (self.preventOverlap([[lx1, ly1, rx2, ry2]])):
                            cv2.line(img, (int(lx1), int(ly1)), (int(lx2), int(ly2)), (255, 50, 50), 8)
                            cv2.line(img, (int(rx1), int(ry1)), (int(rx2), int(ry2)), (255, 50, 50), 8)
                            html.putHtml("<div id=div" + str(self.divNum) + ">")
                            '''
                            html.putCss(html.divCss(self.divNum, html.mappingP(rx1 - lx1, width, False),
                                                    html.mappingP(height, False, height), "\tfloat: left;\n"))
                            '''
                            html.upDivNum(+1)
                            lastDiv=self.divNum-1
                            flag2=True

                        self.makeRows(html, rowGaps, colGaps, img, [[lx1, ly1, rx1, ry1]], [[lx2, ly2, rx2, ry2]])
                        if flag2==True:
                            if lastDiv==self.divNum-1:
                                html.addDivList(id="#div" + str(lastDiv),
                                                width=html.mappingP(rx1 - lx1, width, False),
                                                height=html.mappingP(height, False, height), etc=[{"float":"left"}])
                                cv2.putText(img, "div" + str(lastDiv), (int(lx1) + 10, int(ly1) + 20),
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                            (255, 0, 0), 2)
                                print("div" + str(lastDiv))
                                html.putHtml(fieldSet+str(lastDiv)+"</fieldset>")
                                self.divList.append([["div" + str(lastDiv)], [lx1, ly1, rx2, ry2]])
                            else:
                                html.addDivList(id="#div" + str(lastDiv),
                                                width=html.mappingP(rx1 - lx1, width, False),
                                                height=html.mappingP(height, False, height), etc=[{"float": "left"},{"border":"0px"}])
                            html.putHtml("</div>\n")

                    else:
                        if (self.preventOverlap([[lx1, ly1, rx2, ry2]])):
                            cv2.line(img, (int(lx1), int(ly1)), (int(lx2), int(ly2)), (255, 50, 50), 8)
                            cv2.line(img, (int(rx1), int(ry1)), (int(rx2), int(ry2)), (255, 50, 50), 8)
                            cv2.putText(img, "div" + str(self.divNum), (int(lx1) + 10, int(ly1) + 20),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                        (255, 0, 0), 2)
                            html.putHtml("<div id=div" + str(self.divNum) + ">"+fieldSet+str(self.divNum)+"</fieldset></div>\n")
                            html.addDivList(id="#div" + str(self.divNum),
                                            width=html.mappingP(rx1-lx1,width, False),
                                            height=html.mappingP(height, False, height), etc=[{"float": "left"}])

                            print("div" + str(self.divNum))
                            self.divList.append([["div" + str(self.divNum)], [lx1, ly1, rx2, ry2]])
                            html.upDivNum(+1)
                        pass
                #########################################
                if flag==True:
                    html.putHtml("</div>\n")

            madeRows[i][2]= inCols
            inCols = []
    def log(self,insertL,str):
        if insertL==[[970, 260, 230, 386]]:
            print (str)

    def makeRows(self,html,rows,cols,img,insertL,appendL):
        th = self.threshold
        rows.insert(0,insertL)
        rows.append(appendL)
        madeRows=[]
        tmpRow = []
        for i,trow in enumerate(rows[:-1]):
            opFlag=False
            gaprow=[]
            if trow==tmpRow:
                trow=changeRow
            tx1, ty1, tx2, ty2 = trow[0][0], trow[0][1], trow[0][2], trow[0][3]  # top
            for j,brow in enumerate(rows[i+1:]):
                bx1, by1, bx2, by2 = brow[0][0], brow[0][1], brow[0][2], brow[0][3]  # bottom
                if(abs(tx1-bx1)<th and abs(tx2-bx2)<th)and\
                        (insertL[0][0]-th < bx1 and bx1 < insertL[0][2]+th)and\
                        (insertL[0][0]-th < bx2 and bx2 < insertL[0][2]+th)and\
                        (abs(insertL[0][0]-bx1)<th and abs(insertL[0][2]-bx2)<th):
                    opFlag = True
                    if abs(insertL[0][0]-tx1)<th and abs(insertL[0][0]-bx1)<th:
                        tx1=bx1=insertL[0][0]
                    if abs(insertL[0][2]-tx2)<th and abs(insertL[0][2]-bx2)<th:
                        tx2=bx2=insertL[0][2]
                    break
                elif (abs(tx1-insertL[0][0]<th) and abs(tx2-insertL[0][2]<th))and\
                        ((abs(bx1-insertL[0][0])<th and (insertL[0][2] < bx2))or\
                        (bx1 < insertL[0][0] and abs(insertL[0][2] - bx2) < th)or\
                        (bx1 < insertL[0][0] and insertL[0][2] < bx2)):
                    opFlag = True
                    tx1 = bx1 = insertL[0][0]
                    tx2 = bx2 = insertL[0][2]
                    tmpRow = brow
                    changeRow = [[bx1,by1,bx2,by2]]
                    break
                elif (insertL[0][0]-th < bx1 and bx1 < insertL[0][2]+th)and\
                        (insertL[0][0]-th < bx2 and bx2 < insertL[0][2]+th):
                    gaprow.append(brow)
                opFlag = False
            if opFlag ==True:
                madeRows.append([[tx1,ty1,bx2,by2],gaprow,None])
        self.makeCols(html,madeRows,cols,img,insertL,appendL)

def roi(img,divList,color3=(255,255,255),color1=255):
    minX, minY,maxX,maxY = divList[1][0],divList[1][1],divList[1][2],divList[1][3]
    vertices = np.array([[(minX, minY), (minX, maxY),
                          (maxX, maxY), (maxX, minY)]], dtype=np.int32)
    mask = np.zeros_like(img)
    if len(img.shape) > 2:
        color = color3
    else:
        color = color1
    cv2.fillPoly(mask,vertices,color)
    roiImg= cv2.bitwise_and(img,mask)
    return roiImg

def main(image_src):
    #declare class
    lineMerge=LineMerge()
    getLine = GetLine()
    # -------------preProcessing
    origin = cv2.imread(image_src)
    img = origin.copy()
    #cv2.imshow('orginal',img)
    height,width = img.shape[:2]

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #cv2.imshow("gray",gray)

    ret, edges = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
    edges = cv2.bitwise_not(edges)
    #cv2.imshow("thresh1",thresh1)

    #edges = cv2.Canny(gray, threshold1=50, threshold2=150, apertureSize = 3)
    #cv2.imshow("Canny", edges)
    lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/180, threshold=50,
                            minLineLength=50, maxLineGap=30)
    merged_lines_all = lineMerge.mergeLine(img,lines)

    img_merged_lines = cv2.imread(image_src)
    # ----------find gradient
    rowLines = getLine.limitGradient(merged_lines_all, 185, 175)#Limit degree 185~175
    colLines = getLine.limitGradient(merged_lines_all,95,85)#Limit degree 95~85
    rows=getLine.avgMapping(rowLines,0,img)
    cols=getLine.avgMapping(colLines,1,img)

    ##############

    html = Html(img)
    html.startHtml("test", "test")
    html.makeRows(html,rows,cols,img_merged_lines,[[0, 0, width, 0]],[[0, height, width, height]])
    tmp=""
    for i in html.divCssList:
        tmp += html.makeCssItem(i)
    html.putCss(tmp)
    html.endHtml()
    roiDiv = roi(origin,html.divList[1])
    #cv2.imshow("roi", roiDiv)
    img_merged_lines=cv2.resize(img_merged_lines, None, fx=0.7, fy=0.7, interpolation=cv2.INTER_AREA)
    cv2.imshow("result",img_merged_lines)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

'''-------------------------main------------------------'''
main('test2.jpg')
