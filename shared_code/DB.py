import logging
from datetime import datetime,timedelta, timezone
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
    
    def register(self, blob_url, name, Major, person_id, Mail):
        # new -> create table.
        # exist -> pass create table

        try:
            self.cursor.execute(f"""CREATE TABLE {self.table}(

                id serial PRIMARY KEY,

                images VARCHAR(150) NOT NULL,
                
                name VARCHAR(60) NOT NULL COLLATE utf8mb4_unicode_ci, 

                Major VARCHAR(60) NOT NULL COLLATE utf8mb4_unicode_ci,

                person_id VARCHAR(40)  NOT NULL, 

                Mail VARCHAR(40) NOT NULL,

                enter TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP

                exit TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                
                )""")

            logging.info('succses')
        except:
            logging.info('This table has already exist. Skipped create table process')
            pass
            
        # INSERT
        self.cursor.execute(f"""INSERT INTO {self.table}(images, name, Major, person_id, Mail)

            VALUES("{blob_url}", "{name}", "{Major}", "{person_id}", "{Mail}")
        
        """)

        logging.info('Query OK')

        self.cnx.commit()
        self.cnx.close()

    def select_all(self):
        self.cursor.execute(f"SELECT * FROM {self.table}")
        column = self.cursor.fetchall()

        self.cursor.execute(f"SHOW COLUMNS FROM {self.table}")
        row = self.cursor.fetchall()

        self.cnx.commit()
        self.cnx.close()

        return column, row

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
            self.cursor.execute(f"SELECT name FROM {self.table} WHERE person_id='{id}'")
            name = self.cursor.fetchall() # list?

            # 認識した人が入場するとき
            
            self.cursor.execute(f"UPDATE {self.table} SET `enter`=`{now}`WHERE person_id='{id}'")
            logging.info(f"ようこそ`{name}様(・ω・)ノ")
            
            # 認識した人が退出するとき
            self.cursor.execute(f"UPDATE {self.table} SET `exit`=`{now}`WHERE person_id='{id}'")
            logging.info("またのお越しをお待ちしています(*´▽｀*)")

        # debug
        self.cnx.commit()
        self.cnx.close()

        return name

# 入退場に関してはいらないかも？
    def sendMail(self):
        # properties
        fromAddress = os.environ["MAIL"]
        password = os.environ["MAIL_PASS"]

        subject = "出席確認のお知らせ"
        bodyText  = f"以下の授業の出席を確認しました。\n 授業名：{self.table}"
        for mail in self.mails:
            toAddress = mail

            # auth
            smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
            smtpobj.ehlo()
            smtpobj.starttls()
            smtpobj.ehlo()
            smtpobj.login(fromAddress, password)

            msg = MIMEText(bodyText)
            msg['Subject'] = subject
            msg['From'] = fromAddress
            msg['To'] = toAddress
            msg['Date'] = formatdate()

            smtpobj.sendmail(fromAddress, toAddress, msg.as_string())
            smtpobj.close()