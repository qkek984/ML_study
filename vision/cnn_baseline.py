from keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import Input, Model, layers
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, BatchNormalization
import efficientnet.keras as efn
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing import image
import numpy as np
import pandas as pd

# 랜덤시드 고정시키기
np.random.seed(7)
batch_size =32
img_height=256
img_width=256

train_datagen = ImageDataGenerator(rescale=1./255,
    rotation_range=15,
    shear_range=0.1,
    zoom_range=0.2,
    horizontal_flip=True,
    width_shift_range=0.1,
    height_shift_range=0.1,
    validation_split=0.2)

train_generator = train_datagen.flow_from_directory(
        './train/',
        target_size=(img_height, img_width),
        batch_size=batch_size,
        class_mode='categorical',
        subset='training')

validation_generator = train_datagen.flow_from_directory(
    './train/',
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='categorical',
    subset='validation')

model = efn.EfficientNetB2(include_top=False, input_tensor=Input(shape=(256,256,3)), weights='imagenet')
model.trainable = False #불러온 모델의 웨이트를 학습하지 않도록 설정
x = GlobalAveragePooling2D(name= 'avg_pool')(model.output)
x = BatchNormalization()(x)
x = Dense(1000, activation='softmax')(x)
model = Model(model.input, x)


earlystop = EarlyStopping(patience=5)
checkpoint = ModelCheckpoint("model_eff2.h5",  # file명을 지정합니다
                             monitor='val_loss',  # val_loss 값이 개선되었을때 호출됩니다
                             verbose=1,  # 로그를 출력합니다
                             save_best_only=True,  # 가장 best 값만 저장합니다
                             mode='auto'  # auto는 알아서 best를 찾습니다. min/max
                             )
learning_rate_reduction = ReduceLROnPlateau(
    monitor="val_accuracy",
    patience=2,
    factor=0.5,
    min_lr=0.0001,
    verbose=1)

callbacks = [earlystop, learning_rate_reduction, checkpoint]


epochs = 3
epochs_unfreeze = 10

model.compile(loss="categorical_crossentropy", optimizer=Adam(learning_rate=1e-2, decay=1e-5), metrics=['accuracy'])
model.fit_generator(
        train_generator,
        steps_per_epoch = 39000//batch_size,
        epochs=epochs,
        validation_data = validation_generator,
        validation_steps = 9000//batch_size,
        callbacks = callbacks)

for layer in model.layers[-20:]:
  if not isinstance(layer, layers.BatchNormalization):
    layer.trainable = True# unfreeze
#####
model.compile(loss="categorical_crossentropy", optimizer=Adam(learning_rate=1e-4, decay=1e-5), metrics=['accuracy'])
model.fit_generator(
        train_generator,
        steps_per_epoch = 39000//batch_size,
        epochs=epochs_unfreeze,
        validation_data = validation_generator,
        validation_steps = 9000//batch_size,
        callbacks = callbacks)

model.save_weights("model_eff2.h5")


class_label={}
for key in validation_generator.class_indices:
  class_label[validation_generator.class_indices[key]]=int(key)
print(class_label)


#inference
model.load_weights("model.h5")

data= []
for i in range(72000):
  img = image.load_img("./test/"+str(i)+".jpg", target_size = (256, 256))
  img = image.img_to_array(img)
  img = np.expand_dims(img, axis = 0)
  img /= 255.#학습할때도 리스케일링했으니 예측시에도 적용 안할시 결과가 이상함
  m = model.predict(img)
  m = np.argmax(m, axis=1)
  data.append([str(i)+".jpg", class_label[m[0]]])
  if i%1000==0:
    print(i,"/72000")

submissions = pd.DataFrame(data=data, columns=['filename','prediction'])
submissions.to_csv('submission.csv', index=False)