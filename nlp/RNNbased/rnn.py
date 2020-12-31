import numpy as np
import tensorflow as tf
from tensorflow.python.keras.layers import SimpleRNN,LSTM,Bidirectional

train_X = [[[0.1, 4.2, 1.5, 1.1, 2.8], [1.0, 3.1, 2.5, 0.7, 1.1], [0.3, 2.1, 1.5, 2.1, 0.1], [2.2, 1.4, 0.5, 0.9, 1.1]]]

train_X = np.array(train_X, dtype=np.float32)
print(train_X.shape)
rnn = SimpleRNN(3, return_sequences=True, return_state=True)# return_sequence 모든 시점의 은닉 상태 출력, return_stare 마지막 시점 출력 hidden states와 동일
hidden_state,last_state = rnn(train_X)

print('hidden state : {}, shape: {}'.format(hidden_state, hidden_state.shape))
print('last state : {}, shape: {}'.format(last_state, last_state.shape),"\n")


###### LSTM

lstm = LSTM(3, return_sequences=True, return_state=True)
hidden_state,last_state,last_cell_state = lstm(train_X)
print('hidden state : {}, shape: {}'.format(hidden_state, hidden_state.shape))
print('last hidden state : {}, shape: {}'.format(last_state, last_state.shape))
print('last cell state : {}, shape: {}'.format(last_cell_state, last_cell_state.shape),"\n")


##### Bidirectional LSTM

k_init = tf.keras.initializers.Constant(value=0.1)
b_init = tf.keras.initializers.Constant(value=0)
r_init = tf.keras.initializers.Constant(value=0.1)

bilstm = Bidirectional(LSTM(3, return_sequences=True , return_state=True, kernel_initializer=k_init, bias_initializer=b_init,recurrent_initializer=r_init))#값 비교를 위해 은닉 태 값 고정

hidden_states,forward_h, forward_c, backward_h,backward_c = bilstm(train_X)

print('hidden states : {}, shape: {}'.format(hidden_states, hidden_states.shape))
print('forward state : {}, shape: {}'.format(forward_h, forward_h.shape))
print('backward state : {}, shape: {}'.format(backward_h, backward_h.shape))