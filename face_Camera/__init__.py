import logging
import cv2
import threading
from datetime import datetime
import logging
import azure.functions as func
import os
from shared_code.ui import show_window
from shared_code.DB import MySQL
from shared_code.azure_faceAPI import FaceAPI
from face_Camera.thread.thread_face import FaceThread
import time

def main(req: func.HttpRequest) -> func.HttpResponse:
  
  # get request
  json_data = req.get_json()
  table = json_data['table']

  # connecting Database
  database = MySQL(table)
  images = database.getDBImage()

  # connecting FaceAPI
  face_client = FaceAPI()

# カメラをキャプチャ開始
  cap = cv2.VideoCapture(0)

  while True:
    ret, frame = cap.read()

    #frameを表示
    cv2.imshow('camera capture', frame)

    if(threading.activeCount() == 5):
      th = FaceThread(frame, database, face_client, images)
      th.start()

    #10msecキー入力待ち
    k = cv2.waitKey(1)
    #Escキーを押されたら終了
    if k == 27:
      break

  #キャプチャを終了
  cap.release()
  cv2.destroyAllWindows()

  func.HttpResponse("dummy", status_code=200)

# class FaceThread(threading.Thread):
#   def __init__(self, frame):
#     super(FaceThread, self).__init__()
#     self._cascade_path = "./face_Camera/model_file/haarcascade_frontalface_default.xml"
#     self._frame = frame

#   def run(self):
#     self._frame_gray = cv2.cvtColor(self._frame, cv2.COLOR_BGR2RGB)

#     self._cascade = cv2.CascadeClassifier(self._cascade_path)

#     self._facerect = self._cascade.detectMultiScale(self._frame_gray, scaleFactor=1.2, minNeighbors=3, minSize=(10, 10))

#     if len(self._facerect) > 0:
#       print("detected face")
#       self._color = (255, 255, 255) 
#       for self._rect in self._facerect:
#         cv2.rectangle(self._frame, tuple(self._rect[0:2]),tuple(self._rect[0:2] + self._rect[2:4]), self._color, thickness=2)

#       self._now = datetime.now().strftime('%Y%m%d%H%M%S')
#       self._image_path = self._now + '.jpg'
#       cv2.imwrite(f"/tmp/{self._image_path}", self._frame)
#       print("save")
      
    
# def main(req: func.HttpRequest) -> func.HttpResponse:
  
#   # get request
#   json_data = req.get_json()
#   table = json_data['table']

#   # connecting FacdAPI
#   faceclient = FaceAPI()

#   # connecting Database
#   db = MySQL(table)
#   db_img = db.getDBImage()

#   print("get database image")

#   cap = cv2.VideoCapture(0)

#   while True:
#     ret, frame = cap.read()

#     cv2.imshow("capture", frame)

#     print(threading.activeCount())

#     th = FaceThread(frame)
#     th.start()

#     k = cv2.waitKey(1)
#     if k == 27:
#       break

#     # try:        
#     #   # check log
#     #   print("started recognition")

#     #   person_id = faceclient.recognition(capture_image=img, db_image=db_img)

#     #   if person_id == None:
#     #     continue

#     #   # 番号を引数にしてデータベースを参照、人物の特定を行う
#     #   name = db.upDate(person_id)

#     #   print(name)
#     #   show_window(name)
#   cap.release()
#   cv2.destroyAllWindows()
#     #   # 名前のデータを返す
#   return func.HttpResponse("OK", status_code=200)
#     # except:
#     #   return func.HttpResponse("OpenCVでは顔の検出ができましたがFaceAPIでは検出できませんでした。写真がぶれていた可能性があります", status_code=501)
        
