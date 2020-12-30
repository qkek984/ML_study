import pandas as pd
from sklearn.datasets import fetch_20newsgroups
dataset = fetch_20newsgroups(shuffle=True, random_state=1, remove=('headers', 'footers', 'quotes'))
documents = dataset.data
print(len(documents))
print(dataset.target_names)
print(documents[1])
news_df = pd.DataFrame({'document':documents})
news_df['clean_doc'] = news_df['document'].str.replace("[^a-zA-Z]", " ")#특수문자 제거
news_df['clean_doc'] = news_df['clean_doc'].apply(lambda x: ' '.join([w for w in x.split() if len(w)>3]))# 길이 3이하 제거
news_df['clean_doc'] = news_df['clean_doc'].apply(lambda x: x.lower())# 전체 단어에 대한 소문자 변환
print(news_df['clean_doc'][1])

from nltk.corpus import stopwords
stop_words = stopwords.words('english') # NLTK기반 불용어
tokenized_doc = news_df['clean_doc'].apply(lambda x: x.split()) # 토큰화
tokenized_doc = tokenized_doc.apply(lambda x: [item for item in x if item not in stop_words])

# TF-IDF를 위한 역토큰화
detokenized_doc = []
for i in range(len(news_df)):
    t = ' '.join(tokenized_doc[i])
    detokenized_doc.append(t)

news_df['clean_doc'] = detokenized_doc

#1000개의 단어에 대한 TF-IDF
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer(stop_words='english',
max_features= 1000, # 상위 1,000개의 단어를 보존
max_df = 0.5,
smooth_idf=True)

X = vectorizer.fit_transform(news_df['clean_doc'])
print(X.shape) # TF-IDF 행렬의 크기 확인


#토픽 모델링
from sklearn.decomposition import TruncatedSVD
import numpy as np
svd_model = TruncatedSVD(n_components=20, algorithm='randomized', n_iter=100, random_state=122)
svd_model.fit(X)
print(np.shape(svd_model.components_))


terms = vectorizer.get_feature_names() # 단어 집합. 1,000개의 단어가 저장됨.

def get_topics(components, feature_names, n=5):
    for idx, topic in enumerate(components):
        print("Topic %d:" % (idx+1), [(feature_names[i], topic[i].round(5)) for i in topic.argsort()[:-n - 1:-1]])
get_topics(svd_model.components_,terms)