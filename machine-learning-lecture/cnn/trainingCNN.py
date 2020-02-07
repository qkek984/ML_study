import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers import Dropout
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.preprocessing.image import ImageDataGenerator

# 랜덤시드 고정시키기
np.random.seed(3)

# 1. 데이터 생성하기
train_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
        'result/train',
        target_size=(24, 24),
        color_mode='grayscale',
        batch_size=64,#한번에 64장씩 훈련
        class_mode='categorical')

test_datagen = ImageDataGenerator(rescale=1./255)

test_generator = test_datagen.flow_from_directory(
        'result/test',
        target_size=(24, 24),
        color_mode='grayscale',
        batch_size=64,
        class_mode='categorical')

# 2. 모델 구성하기
model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3),
                 activation='relu',
                 input_shape=(24, 24, 1)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(49, activation='sigmoid'))


# 3. 모델 학습과정 설정하기
#model.compile(loss='sparse_categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
model.compile(loss='binary_crossentropy', optimizer='adam',metrics=['accuracy'])
# 4. 모델 학습시키기

model.fit_generator(
        train_generator,
        steps_per_epoch=150,
        epochs=150,#총 몇번 훈련
        validation_data=test_generator,
        validation_steps=150)

# 6. 모델 평가하기
print("-- Evaluate --")
scores = model.evaluate_generator(test_generator, steps=150)
print(test_generator.filenames)
print("%s: %.2f%%" %(model.metrics_names[1], scores[1]*100))

model.save('model.h5')

# 7. 모델 사용하기
print("-- Predict --")
output = model.predict_generator(test_generator, steps=150)
np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})
print(test_generator.class_indices)
print(output)
