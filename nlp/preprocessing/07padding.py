#numpy로 제로패딩하기
import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
sentences = [['barber', 'person'], ['barber', 'good', 'person'], ['barber', 'huge', 'person'], ['knew', 'secret'], ['secret', 'kept', 'huge', 'secret'], ['huge', 'secret'], ['barber', 'kept', 'word'], ['barber', 'kept', 'word'], ['barber', 'kept', 'secret'], ['keeping', 'keeping', 'huge', 'secret', 'driving', 'barber', 'crazy'], ['barber', 'went', 'huge', 'mountain']]
tokenizer = Tokenizer()
tokenizer.fit_on_texts(sentences)
print(tokenizer.word_index)

encoded = tokenizer.texts_to_sequences(sentences)
print(encoded)
max_len = max(len(item) for item in encoded)
print(max_len)

for item in encoded:
    if len(item) < max_len:
        for _ in range(max_len-len(item)):
            item.append(0)
padded_np = np.array(encoded)
print(padded_np)