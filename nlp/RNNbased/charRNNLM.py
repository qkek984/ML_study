import numpy as np
import urllib.request
import pandas as pd
from string import punctuation
from tensorflow.keras import Sequential
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical
from tensorflow.python.keras.layers import LSTM, TimeDistributed,Dense

urllib.request.urlretrieve("http://www.gutenberg.org/files/11/11-0.txt", filename="11-0.txt")

f = open("11-0.txt",'rb')
lines = []
for l in f:
    l = l.strip()#\r \n 제거
    l = l.lower()
    l=l.decode('ascii','ignore')# \xe2\x80\x99 등과 같은 바이트 열 제거
    if len(l) > 0:
        lines.append(l)
f.close()
text = ' '.join(lines)
print("텍스트샘플",text[:200])


char_vocab = sorted(list(set(text)))
vocab_size = len(char_vocab)
print("글자 집합",char_vocab)
print("글자 집합 길이",len(char_vocab))
char_to_index ={}
for i in range(len(char_vocab)):
    char_to_index[char_vocab[i]] = i
print("char2index",char_to_index)
index_to_char={}
for c in char_to_index:
    index_to_char[char_to_index[c]] = c
print("index2char",index_to_char)

#문장을 샘플화
seq_length = 60
n_samples = int(np.floor((len(text)-1) / seq_length))
print("문장 샘플 갯수: ", n_samples)

train_x = []
train_y = []

for i in range(n_samples):
    x_sample = text[i * seq_length: (i+1)*seq_length]
    x_encoded = [char_to_index[c] for c in x_sample]#정수 인코딩
    train_x.append(x_encoded)

    y_sample = text[i * seq_length+1: (i+1)*seq_length+1]
    y_encoded = [char_to_index[c] for c in y_sample]  # 정수 인코딩
    train_y.append(y_encoded)
print(train_x[0])
print(train_y[0])

#입력 시퀀스에대한 워드 임베딩을 하지 않기 때문에 x데이터도 원핫 인코딩함.
train_x = to_categorical(train_x)
train_y = to_categorical(train_y)
print(train_x.shape)

#모델 설계

model = Sequential()
model.add(LSTM(256, input_shape=(None, train_x.shape[2]),return_sequences=True))
model.add(LSTM(256, return_sequences=True))
model.add(TimeDistributed(Dense(vocab_size,activation='softmax')))

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(train_x,train_y,epochs=80,verbose=2)

def sentence_generation(model, length):
    ix = [np.random.randint(vocab_size)] # 글자에 대한 랜덤 인덱스 생성
    y_char = [index_to_char[ix[-1]]] # 랜덤 익덱스로부터 글자 생성
    print(ix[-1],'번 글자',y_char[-1],'로 예측을 시작!')
    X = np.zeros((1, length, vocab_size)) # (1, length, 55) 크기의 X 생성. 즉, LSTM의 입력 시퀀스 생성

    for i in range(length):
        X[0][i][ix[-1]] = 1 # X[0][i][예측한 글자의 인덱스] = 1, 즉, 예측 글자를 다음 입력 시퀀스에 추가
        print(index_to_char[ix[-1]], end="")
        ix = np.argmax(model.predict(X[:, :i+1, :])[0], 1)
        y_char.append(index_to_char[ix[-1]])
    return ('').join(y_char)

print(sentence_generation(model, 100))