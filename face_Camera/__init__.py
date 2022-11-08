import logging
import cv2
import datetime
import requests
import logging
import azure.functions as func
import os
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face import FaceClient
from shared_code.DB import MySQL
from shared_code.hide_config import KEY, ENDPOINT

def main(req: func.HttpRequest) -> func.HttpResponse:
    face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(1)
    db = MySQL("テーブル名")
    db_img = db.getDBImage()

    faceclient = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))
  
    while True:
      fileName = "photo_" + datetime.datetime.today().strftime('%Y%m%d_%H%M%S') + ".png"
      ret, img1 = cap.read()
      img = cv2.resize(img1, (300, 300), cv2.INTER_AREA)
      gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
      faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

      for x, y, w, h in faces:
        face_gray = gray[y: y + h, x: x + w]

   
        #  ーーpng形式での保存ーー
        picture = cv2.putText(img, 'face detect', (20,50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,0,200), 2, cv2.LINE_AA, cv2.imwrite(fileName, img[y:y+h,x:x+w]))
        # time.sleep(3)
        
        logging.info(db_img)
        # 撮った画像をここで送信する
        try:
            # detect_req_face = faceclient.face.detect_with_stream(send_img, 'detection_03')
            detect_req_face = faceclient.face.detect_with_stream(img, 'detection_03')
            logging.info(len(detect_req_face))
            face_req_id = detect_req_face[0].face_id

            logging.info(face_req_id)

            # それぞれの画像を比較して類似度を分析する
            # 一番類似度が高かった番号を返す
            person_id = 1
            for x in db_img:
                detect_face = faceclient.face.detect_with_url(x, "detection_03")
                face_id = list(map(lambda x: x.face_id, detect_face))
            
                logging.info(face_id)

                similar_faces = faceclient.face.find_similar(face_id=face_req_id, face_ids=face_id)
                if similar_faces:
                    verify_result = faceclient.face.verify_face_to_face(face_id1=face_req_id, face_id2=face_id[0])
                    logging.info("find similar_faces {} = {}. confidence: {}%".format('request_img.png', x, int(verify_result.confidence * 100)))
                    break
                elif person_id < len(db_img):
                    person_id += 1
                    continue
                else:
                    return func.HttpResponse(status_code=201)

            img.close()    
            os.remove('./request_img.png')

            # 番号を引数にしてデータベースを参照、人物の特定を行う
            name = db.upDate(person_id)

            logging.info(name)
            cv2.putText(img,
                text= logging.info(name),
                org=(100, 300),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=1.0,
                color=(0, 255, 0),
                thickness=2,
                lineType=cv2.LINE_4)
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
