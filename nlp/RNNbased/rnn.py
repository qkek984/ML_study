import tensorflow as tf
from tensorflow.python.keras.layers import SimpleRNN

model = tf.keras.Sequential()
model.add(SimpleRNN(3, batch_input_shape=(8,2,10),return_sequences=True))
model.summary()