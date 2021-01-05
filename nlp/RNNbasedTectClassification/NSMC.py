import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import urllib.request
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

from tensorflow.keras.layers import Embedding, Dense, LSTM, Dropout, GRU, Bidirectional
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import load_model
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint



def tokenization(df):
    okt = Okt()
    data = []
    i = 0
    for sentence in df['document']:
        temp = okt.morphs(sentence,stem=True)#한국어 문장 토큰화
        temp = [w for w in temp if w not in stopwords]#불용어 제거
        data.append(temp)
        i+=1
        if i %100 == 0:
            print(i,"/",len(df))
    return data

def sentiment_predict(new_sentence):
    okt=Okt()
    new_sentence = okt.morphs(new_sentence, stem=True) # 토큰화
    new_sentence = [word for word in new_sentence if not word in stopwords] # 불용어 제거
    encoded = tokenizer.texts_to_sequences([new_sentence]) # 정수 인코딩
    pad_new = pad_sequences(encoded, maxlen = max_len) # 패딩
    score = float(loaded_model.predict(pad_new)) # 예측
    if(score > 0.5):
        print("{:.2f}% 확률로 긍정 리뷰입니다.\n".format(score * 100))
    else:
        print("{:.2f}% 확률로 부정 리뷰입니다.\n".format((1 - score) * 100))


urllib.request.urlretrieve("https://raw.githubusercontent.com/e9t/nsmc/master/ratings_train.txt", filename="ratings_train.txt")
urllib.request.urlretrieve("https://raw.githubusercontent.com/e9t/nsmc/master/ratings_test.txt", filename="ratings_test.txt")

train_data = pd.read_table('ratings_train.txt')
test_data = pd.read_table('ratings_test.txt')

print("훈련셋 : ",len(train_data))
print("테스트셋 : ",len(test_data))

print(train_data['document'].nunique(),train_data['label'].nunique())#중복여부 확인

# 중복 데이터 제거
train_data.drop_duplicates(subset=['document'], inplace= True)
test_data.drop_duplicates(subset=['document'], inplace= True)

# Nulll값 제거
train_data['document'].replace('', np.nan, inplace=True)
test_data['document'].replace('', np.nan, inplace=True)
train_data = train_data.dropna(how = 'any')
test_data = test_data.dropna(how = 'any')

# 한글 이외 문자 제거
train_data['document'] = train_data['document'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣]","")
test_data['document'] = test_data['document'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣]","")

print("중복제거 훈련셋 : ",len(train_data))
print("중복제거 테스트셋 : ",len(test_data))

#불용어 정의
stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다']

train_data=train_data[:1000]#샘플 수 1000개로 줄이기
test_data=test_data[:1000]#샘플 수 1000개로 줄이기

#토큰화,불용어제거
X_train = tokenization(train_data)
X_test = tokenization(test_data)
print(X_train[:3])

#정수인코딩
tokenizer = Tokenizer()
tokenizer.fit_on_texts(X_train)
tokenizer.fit_on_texts(X_test)

threshold = 3
total_cnt = len(tokenizer.word_index)
rare_cnt = 0
total_freq = 0
rare_freq = 0

for key,value in tokenizer.word_counts.items():
    total_freq += value# value==등장한 횟수
    if value < threshold:
        rare_cnt += 1
        rare_freq += value

print('단어 집합(vocabulary)의 크기 :',total_cnt)
print('등장 빈도가 %s번 이하인 희귀 단어의 수: %s'%(threshold - 1, rare_cnt))
print("단어 집합에서 희귀 단어의 비율:", (rare_cnt / total_cnt)*100)
print("전체 등장 빈도에서 희귀 단어 등장 빈도 비율:", (rare_freq / total_freq)*100)

#등장빈도 2회 이하인 단어 개수 제거
vocab_size = total_cnt - rare_cnt+2 # 0번패딩과 1번 oov토큰을 고려하여 +2
tokenizer = Tokenizer(vocab_size, oov_token='OOV')# 나머지 토큰은 OOV화 함
tokenizer.fit_on_texts(X_train)

#sequences화
X_train = tokenizer.texts_to_sequences(X_train)
X_test = tokenizer.texts_to_sequences(X_test)

#정답 라벨 저장
y_train = np.array(train_data['label'])
y_test = np.array(test_data['label'])

# 빈도 낮은 단어 제거 후 2차 빈샘플 제거처리
drop_train = [index for index, sentence in enumerate(X_train) if len(sentence) < 1]
X_train = np.delete(X_train, drop_train, axis=0)
y_train = np.delete(y_train, drop_train, axis=0)
print(len(X_train))
print(len(y_train))


#패딩
#길이조사
print('리뷰의 최대 길이 :',max(len(l) for l in X_train))
print('리뷰의 평균 길이 :',sum(map(len, X_train))/len(X_train))
#plt.hist([len(s) for s in X_train], bins=50)
#plt.xlabel('length of samples')
#plt.ylabel('number of samples')
#plt.show()

max_len = 30 # 30으로 할당
X_train = pad_sequences(X_train, maxlen = max_len)
X_test = pad_sequences(X_test, maxlen = max_len)

model = Sequential()
model.add(Embedding(vocab_size, 100))
model.add(GRU(128))
model.add(Dropout(0.1))
model.add(Dense(1, activation='sigmoid'))

es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=4)
mc = ModelCheckpoint('best_model.h5', monitor='val_acc', mode='max', verbose=1, save_best_only=True)

model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['acc'])
history = model.fit(X_train, y_train, epochs=15, callbacks=[es, mc], batch_size=60, validation_split=0.2)

loaded_model = load_model('best_model.h5')
print("\n 테스트 정확도: %.4f" % (loaded_model.evaluate(X_test, y_test)[1]))


##################

#prediction
sentiment_predict('오 영화 핵꿀잼 ㅋㅋㅋㅋ')
sentiment_predict('오 영화 핵꿀노잼 ㅋㅋㅋㅋ')
