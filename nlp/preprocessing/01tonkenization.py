
#### 단어 토큰화

text = "Don't be fooled by the dark sounding name, Mr. Jone's Orphanage is as cheery as cheery goes for a pastry shop."
from nltk.tokenize import word_tokenize
print(word_tokenize(text))
#아포스트로피(')이 상황에 따라 다르게 분리됨

from nltk.tokenize import WordPunctTokenizer
print(WordPunctTokenizer().tokenize(text))
#아포스트로피(')을 일정하게 분리함. WordPunctTokenizer는 구두점을 별도류 분류하는 특징을 가짐

from tensorflow.keras.preprocessing.text import text_to_word_sequence
print(text_to_word_sequence(text))
#아포스트포로피는 단어와함께 보존

from nltk.tokenize import TreebankWordTokenizer
text = "Starting a home-based restaurant may be an ideal. it doesn't have a food chain or restaurant of their own."
print(TreebankWordTokenizer().tokenize(text))
#표준 토큰화방법으로 하이푼 단어는 유지, don't같은 접어는 분리


#### 문장 토큰화
from nltk.tokenize import sent_tokenize
text = "I am actively looking for Ph.D. students. and you are a Ph.D student."
print(sent_tokenize(text))
#Ph.D. 을 문장내의 단어로 인식성공

import kss
text='딥 러닝 자연어 처리가 재밌네요. 하지만 문제는 한국어가 영어보다 너무 어려워요. 농담아니에요. 해보시면 알걸요?'
print(kss.split_sentences(text))


####폼사 태깅
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
#import nltk
#nltk.download('averaged_perceptron_tagger')
text="I am actively looking for Ph.D. students. and you are a Ph.D. student."
print(pos_tag(word_tokenize(text)))

from konlpy.tag import Okt
text ="열심히 코딩한 당신, 연휴에는 여행을 가봐요"
print(Okt().morphs(text))#한국어 폼사태깅
print(Okt().pos(text))#한국어 폼사태깅
print(Okt().nouns(text))#명사만 추출

from konlpy.tag import Kkma
print(Kkma().morphs(text))
print(Kkma().pos(text))
print(Kkma().nouns(text))
