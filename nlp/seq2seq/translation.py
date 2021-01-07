import pandas as pd
import urllib3
import zipfile
import shutil
import os
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical

http = urllib3.PoolManager()
url ='http://www.manythings.org/anki/fra-eng.zip'
filename = 'fra-eng.zip'
path = os.getcwd()
zipfilename = os.path.join(path, filename)
with http.request('GET', url, preload_content=False) as r, open(zipfilename, 'wb') as out_file:
    shutil.copyfileobj(r, out_file)

with zipfile.ZipFile(zipfilename, 'r') as zip_ref:
    zip_ref.extractall(path)

lines = pd.read_csv("fra.txt", names=['src','tar','lic'], sep='\t')
del lines['lic']
print(len(lines))

lines = lines.loc[:,'src':"tar"]
lines = lines[:60000]#샘플수 줄임
lines.tar = lines.tar.apply(lambda x: "\t "+x+" \n")#tar 앞뒤에 심볼 추가
print(lines.sample(10))

#글자 단위 토큰화
src_vocab = set()
for line in lines.src:
    for char in line:
        src_vocab.add(char)
src_vocab = sorted(list(src_vocab))

tar_vocab = set()
for line in lines.tar:
    for char in line:
        tar_vocab.add(char)
tar_vocab = sorted(list(tar_vocab))

src_vocab_size = len(src_vocab)+1
tar_vocab_size = len(tar_vocab)+1
print(src_vocab_size,tar_vocab_size)

src_to_index = dict([(word, i+1) for i, word in enumerate(src_vocab)])
tar_to_index = dict([(word, i+1) for i, word in enumerate(tar_vocab)])
print(src_to_index)

#정수 인코딩
encoder_input = []
for line in lines.src:
    tmp = []
    for w in line:
        tmp.append(src_to_index[w])
    encoder_input.append(tmp)

print(encoder_input[:5])

decoder_input = []
for line in lines.tar:
    tmp = []
    for w in line:
            tmp.append(tar_to_index[w])
    decoder_input.append(tmp)
print(decoder_input[:5])

decoder_target = []
for line in lines.tar:
    t = 0
    tmp = []
    for w in line:
        if t > 0:
            tmp.append(tar_to_index[w])
        t += 1
    decoder_target.append(tmp)
print(decoder_target[:5])

max_src_len = max(len(w) for w in lines.src)
max_tar_len = max(len(w) for w in lines.tar)
print(max_src_len, max_tar_len)

##패딩 추가
encoder_input = pad_sequences(encoder_input,maxlen=max_src_len, padding='post')
decoder_input = pad_sequences(decoder_input,maxlen=max_tar_len, padding='post')
decoder_target = pad_sequences(decoder_target,maxlen=max_tar_len, padding='post')


#원핫 , 글자단위 번역기이므로 워드임베딩 없음
encoder_input = to_categorical(encoder_input)
decoder_input = to_categorical(decoder_input)
decoder_target = to_categorical(decoder_target)

# decoder input이 필요한 이유: teacher focing: 학습시 이전 시점 입력을 사용하는 것이아니라 실제값을 입력으로 사용하여 학습

from tensorflow.keras.layers import Input, LSTM, Embedding,Dense
from tensorflow.keras.models import Model
import numpy as np

#인코더
encoder_inputs = Input(shape=(None,src_vocab_size))
encoder_lstm = LSTM(units=256, return_state=True)#인코더 내부 상태를 넘겨주기 위해 return_state=True
_, state_h, state_c = encoder_lstm(encoder_inputs) # encoder output은 여기서 필요없음
encoder_states = [state_h, state_c]#은닉상태와 셀상태

#디코더
decoder_inputs = Input(shape=(None, tar_vocab_size))
decoder_lstm = LSTM(units=256, return_sequences=True, return_state=True)
decoder_outputs, _, _ = decoder_lstm(decoder_inputs,initial_state=encoder_states)# 초기상태를 인코더 상태로 함
decoder_softmax_layer = Dense(tar_vocab_size, activation='softmax')
decoder_outputs = decoder_softmax_layer(decoder_outputs)

model = Model([encoder_inputs, decoder_inputs], decoder_outputs)
model.compile(optimizer='rmsprop', loss='categorical_crossentropy')

model.fit(x=[encoder_input, decoder_input], y= decoder_target, batch_size=64,epochs=50, validation_split=0.2)
#model.save('trans.h5')


## 기계번역 모델 동작
encoder_model = Model(inputs=encoder_inputs, outputs=encoder_states)

# 이전 시점의 상태들을 저장하는 텐서
decoder_state_input_h = Input(shape=(256,))
decoder_state_input_c = Input(shape=(256,))
decoder_states_inputs = [decoder_state_input_h, decoder_state_input_c]
decoder_outputs, state_h, state_c = decoder_lstm(decoder_inputs, initial_state=decoder_states_inputs)
#  다음 단어를 예측하기 위한 initial_state를 이전 시점의 상태로 사용. 이는 뒤의 함수 decode_sequence()에 구현
decoder_states = [state_h, state_c]# 학습과 달리 LSTM의 은닉 상태와 셀 상태인 state_h와 state_c를 유지
decoder_outputs = decoder_softmax_layer(decoder_outputs)
decoder_model = Model(inputs=[decoder_inputs] + decoder_states_inputs, outputs=[decoder_outputs] + decoder_states)

#인덱스2단어
index_to_src = dict((i, char) for char, i in src_to_index.items())
index_to_tar = dict((i, char) for char, i in tar_to_index.items())

def decode_sequence(input_seq):
    # 입력으로부터 인코더의 상태를 얻음
    states_value = encoder_model.predict(input_seq)

    # <SOS>에 해당하는 원-핫 벡터 생성
    target_seq = np.zeros((1, 1, tar_vocab_size))
    target_seq[0, 0, tar_to_index['\t']] = 1.

    stop_condition = False
    decoded_sentence = ""

    # stop_condition이 True가 될 때까지 루프 반복
    while not stop_condition:
        # 이점 시점의 상태 states_value를 현 시점의 초기 상태로 사용
        output_tokens, h, c = decoder_model.predict([target_seq] + states_value)

        # 예측 결과를 문자로 변환
        sampled_token_index = np.argmax(output_tokens[0, -1, :])
        sampled_char = index_to_tar[sampled_token_index]

        # 현재 시점의 예측 문자를 예측 문장에 추가
        decoded_sentence += sampled_char

        # <eos>에 도달하거나 최대 길이를 넘으면 중단.
        if (sampled_char == '\n' or
           len(decoded_sentence) > max_tar_len):
            stop_condition = True

        # 현재 시점의 예측 결과를 다음 시점의 입력으로 사용하기 위해 저장
        target_seq = np.zeros((1, 1, tar_vocab_size))
        target_seq[0, 0, sampled_token_index] = 1.

        # 현재 시점의 상태를 다음 시점의 상태로 사용하기 위해 저장
        states_value = [h, c]

    return decoded_sentence


for seq_index in [3,50,100,300,1001]: # 입력 문장의 인덱스
    input_seq = encoder_input[seq_index: seq_index + 1]
    decoded_sentence = decode_sequence(input_seq)
    print(35 * "-")
    print('입력 문장:', lines.src[seq_index])
    print('정답 문장:', lines.tar[seq_index][1:len(lines.tar[seq_index])-1]) # '\t'와 '\n'을 빼고 출력
    print('번역기가 번역한 문장:', decoded_sentence[:len(decoded_sentence)-1]) # '\n'을 빼고 출력
