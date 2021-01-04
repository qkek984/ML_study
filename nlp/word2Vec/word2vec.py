import pandas as pd
import matplotlib.pyplot as plt
import urllib.request
from gensim.models.word2vec import Word2Vec
from konlpy.tag import Okt

urllib.request.urlretrieve("https://raw.githubusercontent.com/e9t/nsmc/master/ratings.txt", filename="ratings.txt")
train_data = pd.read_table('ratings.txt')
train_data= train_data[:30000]# 일부 샘플만 적용
print(train_data[:10])

print(train_data.isnull().values.any())#null 값 존재유무
train_data = train_data.dropna(how = 'any')#null 값 존재하는 행 제거
print(train_data.isnull().values.any())#null 값 존재유무 재확인

train_data['document'] = train_data['document'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣]","")#한글이외문자 제거
print(train_data[:10])

#불용어 정의
stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다']

okt = Okt()
tokenized_data=[]
l = len(train_data['document'])
i=0
for sen in train_data['document']:
    tmp_x = okt.morphs(sen,stem=True)
    tmp_x = [w for w in tmp_x if w not in stopwords]
    tokenized_data.append(tmp_x)
    i+=1
    if i%1000==0:
        print(i,"/",l)

print('리뷰의 최대 길이 :',max(len(l) for l in tokenized_data))
print('리뷰의 평균 길이 :',sum(map(len, tokenized_data))/len(tokenized_data))
plt.hist([len(s) for s in tokenized_data], bins=50)
plt.xlabel('length of samples')
plt.ylabel('number of samples')
plt.show()

from gensim.models import Word2Vec
model = Word2Vec(sentences = tokenized_data, size = 100, window = 5, min_count = 5, workers = 4, sg = 0)
print(model.wv.vectors.shape)
print(model.wv.most_similar("최민식"))
print(model.wv.most_similar("히어로"))

model.wv.save_word2vec_format('w2v')