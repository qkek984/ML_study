from sklearn.feature_extraction.text import CountVectorizer
#CountVectorizer는 띄어쓰기기반의 단순 토큰화이기 때문에 한국어에는 제대로 작동하지 않음
corpus = ["Family is not an important thing. It's everything."]

'''#nltk의 불용어 제거
from nltk.corpus import stopwords
sw = stopwords.words("english")
vector = CountVectorizer(stop_words =sw)
'''
#vector = CountVectorizer()
#vector = CountVectorizer(stop_words="english")
vector = CountVectorizer(stop_words=["the", "a", "an", "is", "not"])#사용자 정의 불용어 제거 포함
print(vector.fit_transform(corpus).toarray())
print(vector.vocabulary_)