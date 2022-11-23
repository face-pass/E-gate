import cv2
import base64
import json
import tkinter as tk
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

