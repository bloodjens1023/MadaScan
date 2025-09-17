import os
import pickle

import cv2
import cvzone
import face_recognition
import numpy as np
from  EncodageGenerator import *
from AddDataToDatabase import selection_client



#encodage debut


#fin



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


#importation de l'encodage du fichier
print("chargement du fichier d'encodage ...")


file = open('EncodeFile.p','rb')
EncodingListKnownWithId = pickle.load(file)
file.close()
EncodingListKnown, studentsID = EncodingListKnownWithId
print(studentsID)
print("fichier d'encodage chargé")


modeType = 1
counter = 0
info = []





# --- Définir la zone du bouton juste sous la caméra ---
button_x = 50       # même x que la webcam
button_y = 175 + 480 + 10  # juste en dessous de la caméra + 10px de marge
button_w = 200
button_h = 50

# Fonction pour détecter le clic sur le bouton
def is_button_clicked(event, x, y, flags, param):
    global modeType, counter
    if event == cv2.EVENT_LBUTTONDOWN:
        if button_x <= x <= button_x + button_w and button_y <= y <= button_y + button_h:
            print("Relancer appuyé !")
            modeType = 1
            counter = 0

# Attacher la fonction de clic
cv2.namedWindow('attendue')
cv2.setMouseCallback('attendue', is_button_clicked)

# --- Dans la boucle while, avant cv2.imshow('attendue', imgBack) ---
# Dessiner le bouton sous la caméra
cv2.rectangle(imgBack, (button_x, button_y), (button_x + button_w, button_y + button_h), (0, 123, 255), -1)
cv2.putText(imgBack, "Relancer", (button_x + 40, button_y + 35),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)














while True :
    if modeType==1:
        success, img = cap.read()

    imgS = cv2.resize(img, (0, 0),None,0.25,0.25 )

    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)


    faceCur = face_recognition.face_locations(imgS)
    encodeCur = face_recognition.face_encodings(imgS, faceCur)


    imgBack[175:175 + 480, 50:50 + 640] = img

    resized_img = cv2.resize(imgModList[modeType], (450, 640))  # (largeur, hauteur)


    if counter == 2:
        perso = cv2.imread(f'img/{str(info[0]["image"])}.jpg')
        perso_img = cv2.resize(perso, (250, 250))

        resized_img[105:105 + 250, 95:95 + 250] = perso_img

        cv2.putText(resized_img, str(info[0]["cni"]), (140, 76), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255),
                    2)
        cv2.putText(resized_img, str(info[0]["nom"]), (100, 403), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0),
                    1)
        cv2.putText(resized_img, str(info[0]["prenom"]), (127, 432), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0),
                    1)
        cv2.putText(resized_img, str(info[0]["date_naissance"]), (240, 461), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0),
                    1)
        cv2.putText(resized_img, str(info[0]["lieu_naissance"]), (240, 492), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0),
                    1)
        cv2.putText(resized_img, str(info[0]["domicile"]), (140, 524), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0),
                    1)
        cv2.putText(resized_img, str(info[0]["arrondissement"]), (227, 554), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0),
                    1)
        cv2.putText(resized_img, str(info[0]["profession"]), (160, 588), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0),
                    1)

    imgBack[40:40 + 640, 780:780 + 450] = resized_img  # [y:y+h, x:x+w]

    ids = 0
    for encodeFace, faceLoc in zip(encodeCur, faceCur):

        matches = face_recognition.compare_faces(EncodingListKnown,encodeFace)
        faceDis = face_recognition.face_distance(EncodingListKnown,encodeFace)
        #print("match",matches)
        #print("face distance",faceDis)

        matchIndex = np.argmin(faceDis)
        #print("match",matchIndex)
        y1, x2, y2, x1 = faceLoc
        y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
        bbox = (55 + x1, 162 + y1, x2 - x1, y2 - y1)
        if x1 > 100 and y1  > 100 and x2 < 500 and y2 < 500 :
            imgBack = cvzone.cornerRect(imgBack, bbox, rt=0, t=3)

        if matches[matchIndex] :
            #print(" facial detectée dans la base de données")
            #print(matches[matchIndex])
            if ids != studentsID[matchIndex]:
                ids = studentsID[matchIndex]
                counter = 0
                info = []



            if counter == 0 :
                counter = 1



            if counter != 0 :

                if counter == 1:
                    info = (selection_client(ids))

                    if info:
                        modeType = 0
                        counter += 1
            break
        else:
            counter = 0
            modeType = 2
    #cv2.imshow('webcam', img)




    cv2.imshow('attendue', imgBack)

    cv2.waitKey(1)