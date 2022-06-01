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

                date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                
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

# 修繕の必要あり
    def getProperty(self):

        self.id = []
        self.images = []
        self.person_ids = []
        self.mails = []

        if not self.table:
            logging.error(f"{self.table} table does not exist")
        else:            
            self.cursor.execute(f"SELECT id, images, person_id, Mail FROM {self.table};")
            param_list = self.cursor.fetchall()

            for x in range(len(param_list)):
                self.id.append(param_list[x][0])
                self.images.append(param_list[x][1])
                self.person_ids.append(param_list[x][2])
                self.mails.append(param_list[x][3])
           
            self.student_dic = dict(zip(self.id, self.person_ids))
            self.mail_dic = dict(zip(self.id, self.mails))
            

            # debug
            logging.info(self.mail_dic)

        return self.student_dic, self.images
        
    def upDate(self, person_id):
        flag = 0


        # 今日の日付を求める
        JST = timezone(timedelta(hours=+9), 'JST')
        today = datetime.now(JST)
        today = f"{today:%m/%d}"

        # 指定したテーブルに新しいカラム（今日の日付）を追加する
        # テーブルの中に重複している値がなければ新規追加する
        try:
            self.cursor.execute(f"ALTER TABLE {self.table} ADD `{today}` int NOT NULL;")   
        # 重複していたら追加しない
        except:
            pass

        for id in person_id:
            for ids in self.person_ids:
                if id == ids:
                    flag = 1
                    self.cursor.execute(f"UPDATE {self.table} SET `{today}`={flag} WHERE person_id='{id}'")
                    # debug
                    logging.info("Query OK")
                    self.cnx.commit()
                    self.cnx.close()
                    flag = 0
                else:
                    continue
    
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