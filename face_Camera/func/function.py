import cv2
import base64
import json
import tkinter as tk
import requests
from shared_code.DB import MySQL


def show_window(name):
    root = tk.Tk()
    # サイズ
    root.geometry('500x300')
    # 終了する
    root.after(10000, lambda: root.destroy()) 
    # 表示するもの
    label = tk.Label(root, text=f"ようこそ　{name}さん(*´▽｀*)", font=("",20), bg="#aafaff")  
    label.pack()
    root.mainloop()

def request_1():
    db = MySQL("テーブル名")
    response = requests.post('requestURL', json=db)

    print(response.text)

    if response.status_code == 200:
      show_window(response.text)
    elif response.status_code == 201:
      print("Oops. You are not registered in list")
    elif response.status_code == 501:
      print(response.text)
    else:
      print("Error!! Check the log from azure function")