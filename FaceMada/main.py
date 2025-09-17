import os
import cv2

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


imgBack = cv2.imread('ressources/background.jpg')

pathRes = 'ressources/mod'
modPathList = os.listdir(pathRes)
imgModList = []

for path in modPathList :
    imgModList.append(cv2.imread(os.path.join(pathRes, path)))


#print(len(imgModList))


while True :
    success, img = cap.read()


    imgBack[175:175+480, 50:50+640] = img
    resized_img = cv2.resize(imgModList[1], (450, 640))  # (largeur, hauteur)
    imgBack[40:40 + 640, 780:780 + 450] = resized_img  # [y:y+h, x:x+w]

    #cv2.imshow('webcam', img)
    cv2.imshow('attendue', imgBack)

    cv2.waitKey(1)

