#stopword(불용어) 큰 의미 없는 단어
#import nltk
#nltk.download('stopwords')
from nltk.corpus import stopwords
print(stopwords.words('english')[:10])

#불용어 제거
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
text = "Family is not an important thing. It's everything."
stop_words = set(stopwords.words('english'))
print(stop_words)
word_tokens = word_tokenize(text)
r = []
for w in word_tokens:
    if w not in stop_words:
        r.append(w)
print(word_tokens)
print(r)