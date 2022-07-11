import cv2
import base64
import json
import tkinter as tk

def image_to_json(img):
# ーー　画像を送信可能な形式に変換してJSONに格納　―ー
  _, encimg = cv2.imencode(".png", img)
  img_str = encimg.tostring()
  print(type(img_str))
#  ーー base64形式にする　ーー
  img_byte = base64.b64encode(img_str).decode("utf-8")
  print(type(img_byte))

#  ーー json形式にする ーー
  img_json = json.dumps({'image': img_byte})
  print(type(img_json))

  return img_json

def show_window():
    root = tk.Tk()
    # サイズ
    root.geometry('500x300')
    # 終了する
    root.after(1000, lambda: root.destroy()) 
    # 表示するもの
    label = tk.Label(root, text="ようこそ　〇〇", font=("",20), bg="#aafaff")  
    label.pack()
    root.mainloop()
