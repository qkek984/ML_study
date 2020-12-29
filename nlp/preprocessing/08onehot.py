from konlpy.tag import Okt
okt = Okt()
token = okt.morphs("나는 자연어 처리를 배운다.")
print(token)

word2index={}
for v in token:
    if v not in word2index:
        word2index[v]=len(word2index)
print(word2index)

def one_hot_encoding(word,word2index):
    one_hot_vector = [0]*len(word2index)
    index = word2index[word]
    one_hot_vector[index] = 1
    return one_hot_vector
print(one_hot_encoding("자연어", word2index),"\n")


## 케라스 버전
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.utils import to_categorical
t = Tokenizer()
t.fit_on_texts(["나는 자연어 처리를 배운다."])
print(t.word_index)
encoded = t.texts_to_sequences(["나는 자연어 처리를 배운다."])[0]
print(encoded)
one_hot = to_categorical(encoded)
print(one_hot)
