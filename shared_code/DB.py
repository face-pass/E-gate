import logging
from datetime import datetime,timedelta, timezone
import pymysql
import azure.functions as func
from shared_code.config import config

class MySQL():
    def __init__(self, table):

        self.table = table

        try:
            logging.info("---------------------------")
            self.cnx = pymysql.connect(**db_config)
            logging.info(self.cnx)
            logging.info("Connection established")
        except pymysql.Error as err:
            logging.error(err)

        else:
            self.cursor = self.cnx.cursor()
            logging.info('success')

    def getDBImage(self):

        # 画像を取得
        self.images = []

        if not self.table:
            logging.error(f"table name is empty set!")
        else:            
            self.cursor.execute(f"SELECT images FROM {self.table};")
            param_list = self.cursor.fetchall()

            for x in range(len(param_list)):
                self.images.append(param_list[x][0])

        return self.images

    def Register(self, name):

        for x in range(len(param_list)):
            self.name.append(param_list[x][0])

        self.cursor.execute(f"INSERT {self.table} ({name}, enter, exit, flag) VALUES {self.table}('test', '1', '2', '0')")
        logging.info("registered")

        self.cnx.commit()
        self.cnx.close()

        # 確認
        try:
            logging.info("success")
        except:
            logging.info("error")

        
    def DeleteUser(self, ids):

        self.cursor.execute(f"SELECT id FROM {self.table};")
        param_list = self.cursor.fetchall()

        # idを取得
        for x in ids:
            self.cursor.execute(f"DELETE FROM {self.table} WHERE id = {x}")
        
        self.cnx.commit()
        self.cnx.close()
        
        return func.HttpResponse("deleted user", status_code = 200)

    def upDate(self, person_id):

        # 現在の時刻を調べる
        JST = timezone(timedelta(hours=+9), 'JST')
        now = datetime.now(JST)
        now = now.strftime('%X')

        # idを参照して一致した人の名前を返す
        self.cursor.execute(f"SELECT name, flag FROM {self.table} WHERE id='{person_id}'")
        fetch_one = self.cursor.fetchone()
        name, flag = fetch_one[0], fetch_one[1]

        logging.info(flag)


        if  flag == 0:
            self.cursor.execute(f"UPDATE {self.table} SET `enter`='{now}', `flag`=1 WHERE id={person_id}")
            logging.info(name)

            self.cnx.commit()
            self.cnx.close()

            return name

        elif flag == 1:
            self.cursor.execute(f"UPDATE {self.table} SET `gateway`='{now}', `flag`=0 WHERE id={person_id}")
            logging.info("退場")

            self.cnx.commit()
            self.cnx.close()

            return name

