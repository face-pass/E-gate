import logging
from datetime import datetime,timedelta, timezone
import pymysql
import azure.functions as func
# from shared_code.config import db_config
from shared_code.hide_config import db_config

class MySQL():
    def __init__(self, table):

        self.table = table

        try:
            print("---------------------------")
            self.cnx = pymysql.connect(**db_config)
            self.cursor = self.cnx.cursor()
            print(self.cnx)
            print("Connection established")
        except pymysql.Error as err:
            logging.error(err)

    def getDBImage(self):

        # 画像を取得
        self.images = []

        if not self.table:
            logging.error(f"table name is empty set!")
        else:            
            self.cursor.execute(f"SELECT images FROM {self.table};")
            self.param_list = self.cursor.fetchall()

            for x in range(len(self.param_list)):
                self.images.append(self.param_list[x][0])

        return self.images

    def Register(self, name, image):

        # for x in range(len(self.param_list)):
        #     self.name.append(self.param_list[x][0])

        print(name)


        self.cursor.execute(f"INSERT INTO {self.table} (images, name, enter, gateway, flag) VALUES ('{image}', '{name}', 'test', '1', '0')")
        print("registered")

        self.cnx.commit()
        self.cnx.close()

    def DeleteUser(self, ids):

        self.cursor.execute(f"SELECT id FROM {self.table};")
        self.param_list = self.cursor.fetchall()

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

        print(fetch_one)

        name, flag = fetch_one[0], fetch_one[1]

        print(flag)


        if  flag == 0:
            self.cursor.execute(f"UPDATE {self.table} SET `enter`='{now}', `flag`=1 WHERE id={person_id}")
            print(name)

            self.cnx.commit()
            self.cnx.close()

            return name

        elif flag == 1:
            self.cursor.execute(f"UPDATE {self.table} SET `gateway`='{now}', `flag`=0 WHERE id={person_id}")
            print("退場")

            self.cnx.commit()
            self.cnx.close()

            return name

