import logging
from datetime import datetime,timedelta, timezone
from sqlite3 import Cursor
import pymysql
import os
from shared_code.config import config
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate

class MySQL():
    def __init__(self, table):

        self.table = table

        try:
            logging.info("---------------------------")
            self.cnx = pymysql.connect(**config)
            logging.info(self.cnx)
            logging.info("Connection established")
        except pymysql.Error as err:
            logging.error(err)

        else:
            self.cursor = self.cnx.cursor()
            logging.info('success')

    def getDBImage(self):

        # 取得するのは画像のみ
        self.images = []

        if not self.table:
            logging.error(f"{self.table} table does not exist")
        else:            
            self.cursor.execute(f"SELECT images FROM {self.table};")
            param_list = self.cursor.fetchall()

            for x in param_list:
                self.images.append(param_list[x])
        
        return self.images

    def upDate(self, person_id):

        # 今の時間を調べる
        JST = timezone(timedelta(hours=+9), 'JST')
        now = datetime.now(JST)
        now = f"{now:%h:%m:%s}"

        for id in person_id:
            # idを参照して一致した人の名前を返す
            self.cursor.execute(f"SELECT name, flag FROM {self.table} WHERE person_id='{id}'")
            name = self.cursor.fetchone()
            flag = self.cursor.fetchone()

            if flag == 0:
                self.cursor.execute(f"UPDATE {self.table} SET `enter`=`{now}`, 'flag' = '1' WHERE person_id='{id}'")
                logging.info(f"{name}")

                return name

            elif flag == 1:
                self.cursor.execute(f"UPDATE {self.table} SET `exit`=`{now}`, 'flag' = '0' WHERE person_id='{id}'")
                logging.info("退場")

                return name

        # debug
        self.cnx.commit()
        self.cnx.close()
