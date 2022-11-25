import logging
import azure.functions as func
import os
import cv2
# from config import KEY, ENDPOINT
# from io import BytesIO
# from PIL import Image
from shared_code.hide_config import KEY, ENDPOINT
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
class FaceAPI():

    def __init__(self):
        self.face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))

    def recognition(self, capture_image, db_image):

        image_file = open(capture_image, "rb")
        
        
        detect_req_face = self.face_client.face.detect_with_stream(image_file, detection_model='detection_03', return_face_id=True)
        logging.info(len(detect_req_face))
        face_req_id = detect_req_face[0].face_id
        logging.info(face_req_id)
        # それぞれの画像を比較して類似度を分析する
        # 一番類似度が高かった番号を返す
        person_id = 1
        for image in db_image:

            print(image)

            detect_face = self.face_client.face.detect_with_url(image, detection_model="detection_03", return_face_id=True)

            print(detect_face)

            face_id = list(map(lambda x: x.face_id, detect_face))
        
            # logging.info(face_id)
            # logging.info(face_req_id)

            print(face_id)
            print(face_req_id)


            similar_faces = self.face_client.face.find_similar(face_id=face_req_id, face_ids=face_id)
            if similar_faces:
                verify_result = self.face_client.face.verify_face_to_face(face_id1=face_req_id, face_id2=face_id[0])
                print("find similar_faces {} = {}. confidence: {}%".format('request_img.png', image, int(verify_result.confidence * 100)))
                break
            elif person_id < len(db_image):
                person_id += 1
                continue
            else:
                return func.HttpResponse(status_code=201)
        
        return person_id