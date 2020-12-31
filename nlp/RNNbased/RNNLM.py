from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
from tensorflow.python.keras.utils.np_utils import to_categorical

text=""""경마장에 있는 말이 뛰고 있다\n
그의 말이 법이다\n
가는 말이 고와야 오는 말이 곱다\n"""

#1. 토큰화
t = Tokenizer()
t.fit_on_texts([text])
vocab_size = len(t.word_index)+1#인덱스리턴이니까 +1해줘야 길이임
print(vocab_size)
print(t)
print(t.word_index)

#2.시퀀스화
sequences = list()
for line in text.split('\n'):
    encoded = t.texts_to_sequences([line])[0]
    for i in range(1,len(encoded)):
        sequence = encoded[:i+1]
        sequences.append(sequence)
print(sequences)

#3. 샘플 최대길이로 패딩 추가
max_len = max(len(l) for l in sequences)
print("샘플 최대길이 : ",max_len)
sequences = pad_sequences(sequences, maxlen=max_len,padding='pre')
print(sequences)

#4. 마지막 샘플을 레이블로 분리

x = sequences[:,:-1]
y = sequences[:,-1]
print("x: ",x)
print("y: ",y)

#5.원핫 인코딩
y = to_categorical(y, num_classes=vocab_size)
print("one hot y:", y)

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding,Dense,SimpleRNN

model = Sequential()
model.add(Embedding(vocab_size,10,input_length=max_len-1))#마지막 샘플을 분리했으니 길이는 -1
model.add(SimpleRNN(32))
model.add(Dense(vocab_size,activation="softmax"))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

model.fit(x,y, epochs=200, verbose=2)

def sentence_generation(model, t, current_word, n):
    init_word = current_word
    sentence = ''
    for _ in range(n):
        encoded = t.texts_to_sequences([current_word])[0]#시퀀스화
        print(encoded,"시퀀스화")
        encoded = pad_sequences([encoded], maxlen=5, padding='pre')#패딩추가
        result = model.predict_classes(encoded, verbose=0)#예측

        for word, index in t.word_index.items():
            if index == result:
                break
        current_word += ' '+word
        sentence += ' '+word
    sentence = init_word + sentence
    return sentence

print(sentence_generation(model, t, '경마장에', 4))
print(sentence_generation(model, t, '그의', 2))