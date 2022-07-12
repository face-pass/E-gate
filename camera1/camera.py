from netrc import netrc
import cv2
import datetime
import requests


from func.function import *

#ーーーー顔認識ーーーーー
def save_json(filename, json_image):
    """Python オブジェクトの内容を JSON ファイルに保存します。"""
    with open(filename, 'w', encoding='utf-8', newline='\n') as fp:
      json.dump(json_image, fp)
face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
while True:
  fileName = "photo_" + datetime.datetime.today().strftime('%Y%m%d_%H%M%S') + ".png"
  ret, img = cap.read()
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

  for x, y, w, h in faces:
    face_gray = gray[y: y + h, x: x + w]

    json_image = image_to_json(img)
    
    save_json('output.json', json_image)   
     #  ーーpng形式での保存ーー
    cv2.putText(img, 'face detect', (20,50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,0,200), 2, cv2.LINE_AA, cv2.imwrite(fileName, img))
    # time.sleep(3)

    # 撮った画像をここで送信する
    response = requests.post('', json_image)

    if response.status_code == 200:
      show_window()
    elif response.status_code == 201:
      print("Oops. You are not registered in list")
    else:
      print("Error!! Check requests url or request data")

  cv2.imshow('video image', img)

  key = cv2.waitKey(10)
  if key == 27:
    break
cap.release()
cv2.destroyAllWindows()