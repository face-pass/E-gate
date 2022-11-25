import logging
import cv2
import threading
from io import BytesIO
from datetime import datetime
from shared_code.azure_faceAPI import FaceAPI
from shared_code.DB import MySQL
from shared_code.ui import show_window


class FaceThread(threading.Thread):
    def __init__(self, frame, database, faceclient, image_url):
        super(FaceThread, self).__init__()
        self._cascade_path = "./face_Camera/model_file/haarcascade_frontalface_default.xml"
        self._frame = frame
        self._databse = database
        self._faceclient = faceclient
        self._imageURL = image_url

    def run(self):
        self._frame_gray = cv2.cvtColor(self._frame, cv2.COLOR_BGR2RGB)

        self._cascade = cv2.CascadeClassifier(self._cascade_path)

        self._facerect = self._cascade.detectMultiScale(self._frame_gray, scaleFactor=1.2, minNeighbors=3, minSize=(10, 10))

        if len(self._facerect) > 0:
            self._color = (255, 255, 255)
            for self._rect in self._facerect:
                cv2.putText(self._frame, tuple(self._rect[0:2]), tuple(self._rect[0:2] + self._rect[2:4]), self._color, thickness=2)

            self._now = datetime.now().strftime('%Y%m%d%H%M%S')

            self._image_path = f"./{self._now}.png"
            cv2.imwrite(self._image_path, self._frame)
            person_id = self._faceclient.recognition(self._image_path, self._imageURL)
            print(person_id)
            name = self._databse.upDate(person_id)
            show_window(name)

# get request
# json_data = req.get_json()
table = "test"

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

	if(threading.activeCount() == 1):
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
