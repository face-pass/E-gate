import cv2
import base64
import json
import tkinter as tk

def image_to_json(img):
# ーー　画像を送信可能な形式に変換してJSONに格納　―ー
  _, encimg = cv2.imencode(".png", img)
  img_str = encimg.tostring()
  
#  ーー base64形式にする　ーー
  img_byte = base64.b64encode(img_str).decode("utf-8")

#  ーー json形式にする ーー
  img_json = {'table': 'test','image': img_byte}

  return img_json

def show_window(name):
    root = tk.Tk()
    # サイズ
    root.geometry('500x300')
    # 終了する
    root.after(4000, lambda: root.destroy()) 
    # 表示するもの
    label = tk.Label(root, text=f"ようこそ　{name}さん", font=("",20), bg="#aafaff")  
    label.pack()
    root.mainloop()
