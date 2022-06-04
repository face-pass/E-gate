from base64 import b64decode
import logging
import cv2
import pymysql
import io
import json
import azure.functions as func
import os
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face import FaceClient
from shared_code.image_decoder import img_decoder
from shared_code.DB import MySQL

ENDPOINT = os.environ['ENDPOINT']
KEY = os.environ['KEY']

def main(req: func.HttpRequest) -> func.HttpResponse:

    faceclient = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))

    logging.info('Python HTTP trigger function processed a request.')

    # json形式で送られてきたデータを受け取る
    try:
        table = req.get_json('table')
        b64_data = req.get_json('b64')
    except:
        return func.HttpResponse('table or b64_data does not exist')

    # 送られてきたデータ(バイナリデータ)を画像データに変換する
    send_img = img_decoder(b64_data)

    # データベースに接続して画像データをリストとして持ってくる
    db = MySQL(table)
    db_img = db.getDBImage()

    detect_req_face = faceclient.face.detect_with_stream(send_img, 'detection_03')
    face_req_id = detect_req_face.face_id

    # それぞれの画像を比較して類似度を分析する
    # 一番類似度が高かった番号を返す
    person_id = 1
    for x in db_img:
        detect_face = faceclient.face.detect_with_url(x, "detection_03")
        face_id = detect_face.face_id

        similar_faces = faceclient.face.find_similar(face_id=face_id, face_ids=face_req_id)
        if similar_faces:
            verify_result = faceclient.face.verify_face_to_face(face_id1=face_id, face_id2=face_req_id)
            logging.info("find similar_faces {} = {}. confidence: {}%".format(x, send_img, int(verify_result.confidence * 100)))
            break
        else:
            person_id += 1
            continue
    
    # 番号を引数にしてデータベースを参照、人物の特定を行う
    name = db.upDate(person_id)

    # 名前のデータを返す
    return func.HttpResponse(name, status_code=200)