from pickle import NEXT_BUFFER
from keras.models import load_model
from enum import Enum
from time import sleep
from keras_preprocessing.image import img_to_array
from keras_preprocessing import image
import cv2
import numpy as np
import math
import time

face_classifier=cv2.CascadeClassifier('/home/raspberry/R3LAX-M4X/EmotionDetection/haarcascade_frontalface_default.xml')
classifier = load_model('/home/raspberry/R3LAX-M4X/EmotionDetection/EmotionDetectionModel.h5')

class_labels=['Angry','Happy','Neutral','Sad','Surprise']

class Labels(Enum):
    Angry = 0
    Sad = 1
    Neutral = 2
    Surprise = 3
    Happy = 4

def abc(context):
    t0 = None

    while not context[0]:
        if t0 is None or context[1] or (time.time_ns() - t0) / 1000000.0 > (1000.0 * 60.0):
            context[4].acquire()
            context[2] = True
            cap=cv2.VideoCapture(0)

            nbFrames=60
            tabLabel = []

            for i in range(nbFrames):
                ret,frame=cap.read()
                labels=[]
                gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                faces=face_classifier.detectMultiScale(gray,1.3,5)
                label = 'Neutral'

                for (x,y,w,h) in faces:
                    cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
                    roi_gray=gray[y:y+h,x:x+w]
                    roi_gray=cv2.resize(roi_gray,(48,48),interpolation=cv2.INTER_AREA)

                    if np.sum([roi_gray])!=0:
                        roi=roi_gray.astype('float')/255.0
                        roi=img_to_array(roi)
                        roi=np.expand_dims(roi,axis=0)

                        preds=classifier.predict(roi)[0]
                        label=class_labels[preds.argmax()]
                        label_position=(x,y)


                tabLabel.append(Labels[label].value)


            context[3] = np.mean(tabLabel)
            context[4].release()
            cap.release()
            cv2.destroyAllWindows()
            t0 = time.time_ns()
