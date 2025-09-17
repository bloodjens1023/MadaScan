
import cv2
import face_recognition
import os
import pickle


pathRes = 'img'
PathList = os.listdir(pathRes)
imgList = []
studentsID = []


for path in PathList :
    imgList.append(cv2.imread(os.path.join(pathRes, path)))
    studentsID.append(os.path.splitext(path)[0])

print(studentsID)


def TrouverEncodage(ImagesList):
    encodeList =[]
    for img in ImagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList

print("encoding start")
EncodingListKnown = TrouverEncodage(imgList)
EncodingListKnownWithId = [EncodingListKnown, studentsID]
print("encoding end")


file = open('EncodeFile.p', 'wb')
pickle.dump(EncodingListKnownWithId, file)
file.close()
print("file saved")
