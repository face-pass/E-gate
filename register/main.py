import sys, os
sys.path.append(os.pardir)
from shared_code.config import config
import pymysql

cnx = pymysql.connect(**config)
print("login")
cursor = cnx.cursor()

img_url = 'image_url'
name = 'your name'

cursor.execute(f'insert into test(images, name, enter, gateway) values("{img_url}", "{name}", "test", "test");')
print("register")

cnx.commit()
cnx.close()