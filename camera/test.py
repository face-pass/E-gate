import cv2
import datetime
import time
import base64
import json

from cv2 import IMWRITE_JPEG2000_COMPRESSION_X1000




# ーーーー顔認識ーーーーー
face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
while True:
    fileName = "photo_" + datetime.datetime.today().strftime('%Y%m%d_%H%M%S') + ".jpg"
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.3, minNeighbors=5)
    for x, y, w, h in faces:
        # cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2).T
        # face = img[y: y + h, x: x + w]
        face_gray = gray[y: y + h, x: x + w]
        dst_str = base64.b64encode(img)        
        image = dst_str.decode('utf-8')
        #print(type(img_json))
        img_json = {'image': image}
        # print(img_json + "awljforslgjz\n")
        cv2.putText(img, 'face detect', (20, 50), cv2.FONT_HERSHEY_SIMPLEX,
                    1.2, (0, 0, 200), 2, cv2.LINE_AA, cv2.imwrite(fileName, img))
        time.sleep(5)
        print(type(img_json))

    cv2.imshow('video image', img)
    # if faces :
    #   cv2.imwrite(fileName, img)

    key = cv2.waitKey(10)
    if key == 27:
        break
cap.release()
cv2.destroyAllWindows()
