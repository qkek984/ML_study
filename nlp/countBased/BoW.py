from konlpy.tag import Okt
import re
okt = Okt()
text="정부가 발표하는 물가상승률과 소비자가 느끼는 물가상승률은 다르다."
token= re.sub("(\.)","",text)
token = okt.morphs(token)#토큰화
print(token)

word2index={}
bow=[]#빈도 저장
for t in token:
    if t not in word2index:
        word2index[t]= len(word2index)
        bow.append(1)
    else:
        bow[word2index[t]] += 1
print(word2index)
print(bow)
