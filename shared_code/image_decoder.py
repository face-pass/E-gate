import numpy as np
import base64
import cv2

def img_decoder(b64_data):
    #バイナリデータ <- base64でエンコードされたデータ  
    img_binary = base64.b64decode(b64_data)
    jpg=np.frombuffer(img_binary,dtype=np.uint8)

    # row Image -> image
    img = cv2.imdecode(jpg, cv2.IMREAD_COLOR)

    return img