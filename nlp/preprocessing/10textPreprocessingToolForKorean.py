#####띄어쓰기
sent ="아버지가방에들어가신다."
from pykospacing import spacing
k_sent = spacing(sent)
print(k_sent)


#####맞춤법 교정
from hanspell import spell_checker

sent ="맞춤법 틀리면 외 않되? 쓰고싶은대로쓰면돼지"
s_sent = spell_checker.check(sent)
print(s_sent.checked)

#####학습을 통한 단어 토큰화
import urllib.request
from soynlp import DoublespaceLineCorpus
from soynlp.word import WordExtractor

urllib.request.urlretrieve("https://raw.githubusercontent.com/lovit/soynlp/master/tutorials/2016-10-20.txt", filename="2016-10-20.txt")

corpus = DoublespaceLineCorpus("2016-10-20.txt")
print(len(corpus))

i = 0
for document in corpus:
  if len(document) > 0:
    print(document)
    i = i+1
  if i == 3:
    break

word_extractor = WordExtractor()
word_extractor.train(corpus)
word_score_table = word_extractor.extract()

print(word_score_table["반포한"].cohesion_forward)
print(word_score_table["반포한강"].cohesion_forward)
print(word_score_table["반포한강공원"].cohesion_forward)

##### 최대 점수 토크나이저를 통한 띄어쓰기 토큰화
from soynlp.tokenizer import LTokenizer

scores = {word:score.cohesion_forward for word, score in word_score_table.items()}
l_tokenizer = LTokenizer(scores=scores)
l_tokenizer.tokenize("국제사회와 우리의 노력들로 범죄를 척결하자", flatten=False)

from soynlp.tokenizer import MaxScoreTokenizer

maxscore_tokenizer = MaxScoreTokenizer(scores=scores)
maxscore_tokenizer.tokenize("국제사회와우리의노력들로범죄를척결하자")


## 반복문자 정제
from soynlp.normalizer import *
print(emoticon_normalize('앜ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ이영화존잼쓰ㅠㅠㅠㅠㅠㅠ', num_repeats=2))


## costomized KoNLPy
from ckonlpy.tag import Twitter
twitter = Twitter()
print(twitter.morphs('은경이는 사무실로 갔습니다.'))
twitter.add_dictionary('은경이', 'Noun')
print(twitter.morphs('은경이는 사무실로 갔습니다.'))