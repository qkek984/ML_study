#####Lemmatization (표제어추츨)
# am are is -> be

#import nltk
#nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer

words=['policy', 'doing', 'organization', 'have', 'going', 'love', 'lives', 'fly', 'dies', 'watched', 'has', 'starting']
print([WordNetLemmatizer().lemmatize(w) for w in words])
#단어의 품사정보를 알아야만 정확한 결과를 얻을수있기때문에 dy ha 와 같은 결과도 출력함
print(WordNetLemmatizer().lemmatize('dies','v'))#정확함 품사를 함께 입력


#####stemming (어간추출)
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
text ="This was not the map we found in Billy Bones's chest, but an accurate copy, complete in all things--names and heights and soundings--with the single exception of the red crosses and the written notes."
words = word_tokenize(text)
print(words)

print([PorterStemmer().stem(w) for w in words])

words=['formalize', 'allowance', 'electricical']
print([PorterStemmer().stem(w) for w in words])

from nltk.stem import LancasterStemmer
words=['policy', 'doing', 'organization', 'have', 'going', 'love', 'lives', 'fly', 'dies', 'watched', 'has', 'starting']
print([PorterStemmer().stem(w) for w in words])
print([LancasterStemmer().stem(w) for w in words])