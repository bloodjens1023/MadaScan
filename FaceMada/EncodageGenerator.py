
import cv2
import face_recognition
import os
import pickle


pathRes = 'img'
modPathList = os.listdir(pathRes)
imgList = []

for path in modPathList :
    imgList.append(cv2.imread(os.path.join(pathRes, path)))


print(len(imgList))