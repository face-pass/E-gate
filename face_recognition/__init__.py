import logging
import azure.functions as func
import os
from PIL import Image
# from shared_code.image_decoder import img_decoder
from shared_code.DB import MySQL
from shared_code.azure_faceAPI import FaceAPI

def main(req: func.HttpRequest) -> func.HttpResponse:

    # Connecting MySQL
    database = MySQL()
    db_image = database.getDBImage()

    # Connecting FaceAPI
    face_api = FaceAPI()

    logging.info('Python HTTP trigger function processed a request.')

    # リクエスト処理の最適化を行う
    # json_data = req.get_json()
    # table = json_data['table']
    # b64_data = json_data['image']

    method = req.method
    images = req.files.getlist("images")
    form = req.form

    # check request data
    if not all([images, form]):
        logging.error("Error!! Please check response")
        return func.HttpResponse("image or form data does not exist", status_code=400)
    
    # check image file format
    elif not all([images.filename.endswith(".jpg")]) or all([images.filename.endswith(".png")]):
        logging.error("Error!! Please check response")
        return func.HttpResponse("Only png or jpg image formats are supported", status_code=400) 


    # 送られてきたデータ(バイナリデータ)を画像データに変換する
    # send_img = img_decoder(b64_data)
    # pil_img = Image.fromarray(send_img)
    # pil_img.save('./request_img.png')
    try:

        for image in images:
            person_id = face_api.recognition(image, db_image)

        # try:
        #     # detect_req_face = faceclient.face.detect_with_stream(send_img, 'detection_03')
        #     detect_req_face = faceclient.face.detect_with_stream(img, 'detection_03')
        #     logging.info(len(detect_req_face))
        #     face_req_id = detect_req_face[0].face_id

        #     logging.info(face_req_id)

        #     # それぞれの画像を比較して類似度を分析する
        #     # 一番類似度が高かった番号を返す
        #     person_id = 1
        #     for x in db_img:
        #         detect_face = faceclient.face.detect_with_url(x, "detection_03")
        #         face_id = list(map(lambda x: x.face_id, detect_face))

        #         logging.info(face_id)

        #         similar_faces = faceclient.face.find_similar(face_id=face_req_id, face_ids=face_id)
        #         if similar_faces:
        #             verify_result = faceclient.face.verify_face_to_face(face_id1=face_req_id, face_id2=face_id[0])
        #             logging.info("find similar_faces {} = {}. confidence: {}%".format('request_img.png', x, int(verify_result.confidence * 100)))
        #             break
        #         elif person_id < len(db_img):
        #             person_id += 1
        #             continue
        #         else:
        #             return func.HttpResponse(status_code=201)

            # 番号を引数にしてデータベースを参照、人物の特定を行う
        name = database.upDate(person_id)

        logging.info(name)

        # 名前のデータを返す
        return func.HttpResponse(name, status_code=200)
    except:
        return func.HttpResponse("Internal Server Error", status_code=500)