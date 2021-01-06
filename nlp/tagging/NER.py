import re
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
import numpy as np

f = open('train.txt','r')
tagged_sentences = []
sentence = []

for line in f:
    if len(line) == 0 or line.startswith('-DOCSTART') or line[0] == '\n':
        if len(sentence)>0:
            tagged_sentences.append(sentence)
            sentence = []
        continue
    #첫행:단어, 끝행:개체명 데이터만 사용할것임
    splits = line.split(' ')
    splits[-1] = re.sub(r'\n', '', splits[-1])#줄바꿈표시 제거
    word = splits[0].lower()
    sentence.append([word,splits[-1]])

print("전체 샘플 개수", len(tagged_sentences))
print("첫 샘플: ", tagged_sentences[0])

sentences,ner_Tag =[],[]

for ts in tagged_sentences:
    sen, ner = zip(*ts)
    sentences.append(list(sen))
    ner_Tag.append(list(ner))
print(sentences[0])
print(ner_Tag[0])

###길이 분석
print('샘플의 최대 길이 : %d' % max(len(l) for l in sentences))
print('샘플의 평균 길이 : %f' % (sum(map(len, sentences))/len(sentences)))
plt.hist([len(s) for s in sentences], bins=50)
plt.xlabel('length of samples')
plt.ylabel('number of samples')
#plt.show()

max_words = 4000# 상위 4000개의 집합만 사용
src_tokenizer = Tokenizer(num_words=max_words, oov_token='OOV')
src_tokenizer.fit_on_texts(sentences)

tar_tokenizer = Tokenizer()
tar_tokenizer.fit_on_texts(ner_Tag)

vocab_size = max_words
tag_size = len(tar_tokenizer.word_index) + 1

print('단어 집합의 크기 : {}'.format(vocab_size))
print('개체명 태깅 정보 집합의 크기 : {}'.format(tag_size))

#정수 인코딩
x_train = src_tokenizer.texts_to_sequences(sentences)
y_train = tar_tokenizer.texts_to_sequences(ner_Tag)
print(x_train[0])
print(y_train[0])

index_to_word = src_tokenizer.index_word
index_to_ner = tar_tokenizer.index_word

max_len = 60
x_train = pad_sequences(x_train,padding='post',maxlen=max_len)
y_train = pad_sequences(y_train,padding='post',maxlen=max_len)

x_train,x_test,y_train,y_test = train_test_split(x_train,y_train,test_size=.2, random_state=777)

y_train= to_categorical(y_train,num_classes=tag_size)
y_test= to_categorical(y_test,num_classes=tag_size)

print('훈련 샘플 문장의 크기 : {}'.format(x_train.shape))
print('훈련 샘플 레이블의 크기 : {}'.format(y_train.shape))
print('테스트 샘플 문장의 크기 : {}'.format(x_test.shape))
print('테스트 샘플 레이블의 크기 : {}'.format(y_test.shape))

from keras.models import Sequential
from keras.layers import Dense, Embedding, LSTM, Bidirectional, TimeDistributed
from keras.optimizers import Adam

model = Sequential()
model.add(Embedding(input_dim=vocab_size, output_dim=128, input_length=max_len, mask_zero=True))
model.add(Bidirectional(LSTM(256, return_sequences=True)))#다 대 다 구조로 return_sequences True설정
model.add(TimeDistributed(Dense(tag_size, activation='softmax')))

model.compile(loss='categorical_crossentropy', optimizer=Adam(0.001), metrics=['accuracy'])

model.fit(x_train, y_train, batch_size=128, epochs=8,  validation_data=(x_test, y_test))

print("\n 테스트 정확도: %.4f" % (model.evaluate(x_test, y_test)[1]))


i=10 # 확인하고 싶은 테스트용 샘플의 인덱스.
y_predicted = model.predict(np.array([x_test[i]])) # 입력한 테스트용 샘플에 대해서 예측 y를 리턴
y_predicted = np.argmax(y_predicted, axis=-1) # 원-핫 인코딩을 다시 정수 인코딩으로 변경함.
true = np.argmax(y_test[i], -1) # 원-핫 인코딩을 다시 정수 인코딩으로 변경함.

print("{:15}|{:5}|{}".format("단어", "실제값", "예측값"))
print(35 * "-")

for w, t, pred in zip(x_test[i], true, y_predicted[0]):
    if w != 0: # PAD값은 제외함.
        print("{:17}: {:7} {}".format(index_to_word[w], index_to_ner[t].upper(), index_to_ner[pred].upper()))