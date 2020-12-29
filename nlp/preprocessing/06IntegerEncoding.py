from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

text = "A barber is a person. a barber is good person. a barber is huge person. he Knew A Secret! The Secret He Kept is huge secret. Huge secret. His barber kept his word. a barber kept his word. His barber kept his secret. But keeping and keeping such a huge secret to himself was driving the barber crazy. the barber went up a huge mountain."

vocab = {}
sentences = []
stop_words = set(stopwords.words('english'))

text = sent_tokenize(text)

for i in text:
    sentence = word_tokenize(i)
    result = []
    for w in sentence:
        w = w.lower()
        if w not in stop_words:
            if len(w)>2:
                result.append(w)
                if w not in vocab:
                    vocab[w] = 1
                else:
                    vocab[w] += 1
    sentences.append(result)

for i in sentences:
    print(i)

#높은 빈도수대로 정렬
vocab_sorted = sorted(vocab.items(), key = lambda x:x[1], reverse = True)

word_to_index = {}
#상위 5개 글자만 저장
for i in range(5):
    word_to_index[vocab_sorted[i][0]] = i+1
word_to_index['OOV'] = len(word_to_index)+1
print(word_to_index)

#정수로 인코딩
encoded =[]
for s in sentences:
    tmp=[]
    for w in s:
        if w in word_to_index:
            tmp.append(word_to_index[w])
        else:
            tmp.append(word_to_index['OOV'])
    encoded.append(tmp)
print(encoded)

#NLTK의 FreqDist, keras의 word_counts도 이용 가능