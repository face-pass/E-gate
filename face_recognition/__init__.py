from base64 import b64decode
import logging
import cv2
import pymysql
import io
import json
import azure.functions as func
from shared_code.image_decoder import img_decoder
from shared_code.DB import MySQL

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # json形式で送られてきたデータを受け取る
    table = req.get_json('table')
    b64_data = req.get_json('b64')

    # 送られてきたデータ(バイナリデータ)を画像データに変換する
    send_img = img_decoder(b64_data)

    # データベースに接続して画像データをリストとして持ってくる
    db = MySQL(table)
    db_img = db.

    # それぞれの画像を比較して類似度を分析する

    # 一番類似度が高かった番号を返す

    # 番号を引数にしてデータベースを参照、人物の特定を行う

    # 名前のデータを返す

    
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
