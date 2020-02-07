import glob

import cv2
from keras.models import load_model
from keras.preprocessing import image
import numpy as np
from keras.preprocessing.image import ImageDataGenerator


class predictCNN:
    def __init__(self):
        self. predictionLabel = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
         '아', '바', '버', '보', '부', '다', '도', '두', '가', '거',
         '고', '구', '하', '허', '호', '자', '저', '조', '라', '러',
         '마', '머', '모', '무', '나', '너', '노', '누', '오', '로',
         '루', '사', '서', '소', '수', '더', '어', '우', '주']
        # dimensions of our images
        self.size = (24, 24)
        # load the model we saved
        self.model = load_model('model.h5')
        #self.model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
        #self.model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
        self.model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        #self.model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    def predict(self,inputImg):
        # predicting images
        #img = image.load_img(inputImg, target_size=(self.img_width, self.img_height))
        img = cv2.resize(inputImg, self.size)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        images = np.vstack([x])
        classes = self.model.predict_classes(images)########################################
        index= int(classes[0])

        ev = self.model.predict_proba(x)
        probability = ev[0][index]
        #print("index:", str(index))


        return self.predictionLabel[classes[0]],probability

if __name__=='__main__':
    #inputImg='./result/test/ger/1543199873.0831523.png'
    #inputImg = cv2.imread('./result/test/ger/1543199873.0831523.png')
    prediccnn = predictCNN()#함수 선언 및 할당

    #target_dir = "result/test/3/"  # 지정할 디렉토리 경로
    #target_dir = "val/"  # 지정할 디렉토리 경로
    target_dir = "KVLPC/2/"  # 지정할 디렉토리 경로
    files = glob.glob(target_dir + "*.*")
    #print(files)

    error=0
    for i,file in enumerate(files):
        inputImg = cv2.imread(file)

        prediction,probability = prediccnn.predict(inputImg)
        print("<file Name : ", file,">")
        print("predict : ",prediction)
        print("prob :", probability)
        print("--------")

        if prediction != "2" :
            error+=1
    print("==============================")
    print("total : ", len(files))
    print("error : ", error)
    print("acc : ", float(100)-float(error/len(files)*100))




