import logging
import azure.functions as func
from config import KEY, ENDPOINT
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
class FaceAPI():

    def __init__(self):
        self.face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))

    def recognition(self, capture_image, db_image):

        detect_req_face = self.face_client.face.detect_with_stream(capture_image, 'detection_03')
        logging.info(len(detect_req_face))

        face_req_id = detect_req_face[0].face_id
        logging.info(face_req_id)

        # それぞれの画像を比較して類似度を分析する
        # 一番類似度が高かった番号を返す
        person_id = 1
        for image in db_image:
            detect_face = self.faceclient.face.detect_with_url(image, "detection_03")
            face_id = list(map(lambda x: x.face_id, detect_face))
        
            logging.info(face_id)

            similar_faces = self.faceclient.face.find_similar(face_id=face_req_id, face_ids=face_id)
            if similar_faces:
                verify_result = self.faceclient.face.verify_face_to_face(face_id1=face_req_id, face_id2=face_id[0])
                logging.info("find similar_faces {} = {}. confidence: {}%".format('request_img.png', image, int(verify_result.confidence * 100)))
                break
            elif person_id < len(db_image):
                person_id += 1
                continue
            else:
                return func.HttpResponse(status_code=201)