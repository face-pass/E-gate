import logging
import cv2
import datetime
import logging
import azure.functions as func
import os

from shared_code.DB import MySQL
from shared_code.azure_faceAPI import FaceAPI
from func.function import show_window
def main(req: func.HttpRequest) -> func.HttpResponse:
    json_data = req.get_json()
    table = json_data['table']
    db = MySQL(table)
    db_img = db.getDBImage()

    face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(1)
    
    faceclient = FaceAPI()
    
    while True:
      fileName = "photo_" + datetime.datetime.today().strftime('%Y%m%d_%H%M%S') + ".png"
      ret, img1 = cap.read()
      img = cv2.resize(img1, (300, 300), cv2.INTER_AREA)
      faces = face_cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=5)

      # for x, y, w, h in faces:
        # x, y, w, h = faces
        # face_gray = img[y: y + h, x: x + w]
      # picture = cv2.puttext(img, 'face detect' (20,50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,0,200), 2, cv2.LONE_AA,cv2.imwrite(fileName, img[y:y+h,x:x+w]))
      logging.info(db_img)
      # 撮った画像をここで送信する
      try:
          person_id = faceclient.recognition(capture_image=img, db_image=db_img)

          img.close()    
          os.remove('./request_img.png')

          # 番号を引数にしてデータベースを参照、人物の特定を行う
          name = db.upDate(person_id)

          logging.info(name)
          show_window(name)
          # 名前のデータを返す
          return func.HttpResponse(name, status_code=200)
      except:
          return func.HttpResponse("OpenCVでは顔の検出ができましたがFaceAPIでは検出できませんでした。写真がぶれていた可能性があります", status_code=501)

      cv2.imshow('video image', img)

      key = cv2.waitKey(10)
      if key == 27:
        break
    cap.release()
    cv2.destroyAllWindows()
