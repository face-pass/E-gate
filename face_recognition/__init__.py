import logging
import azure.functions as func
import os
from PIL import Image
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face import FaceClient
from shared_code.image_decoder import img_decoder
from shared_code.DB import MySQL

ENDPOINT = ""
KEY = ""

def main(req: func.HttpRequest) -> func.HttpResponse:

    faceclient = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))

    logging.info('Python HTTP trigger function processed a request.')

    # json形式で送られてきたデータを受け取る
    try:
        json_data = req.get_json()
        table = json_data['table']
        b64_data = json_data['image']

        # logging.info(json_data)
        # logging.info(table)
        # logging.info(b64_data)
    except:
        func.HttpResponse("Error!! Please check json_data, table, b64_data.", status_code=400)
    # 送られてきたデータ(バイナリデータ)を画像データに変換する
    send_img = img_decoder(b64_data)
    pil_img = Image.fromarray(send_img)
    pil_img.save('./request_img.png')

    # データベースに接続して画像データをリストとして持ってくる
    db = MySQL(table)
    db_img = db.getDBImage()

    logging.info(db_img)

    img = open('./request_img.png', 'rb')

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

        # 名前のデータを返す
        return func.HttpResponse(name, status_code=200)
    except:
        return func.HttpResponse("OpenCVでは顔の検出ができましたがFaceAPIでは検出できませんでした。写真がぶれていた可能性があります", status_code=501)