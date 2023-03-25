import logging
import azure.functions as func
import json
from shared_code.DB import MySQL

table = "test" #　ここはのちにpostリクエストでパラメータを受け取れるように変更する

data_list_key = []
data_list = []

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    mysql = MySQL(table)

    # get current attandance list from mysql
    allData = mysql.getAllData()

    logging.info(allData)
    
    for x in range(len(allData)):
        data_list.append(allData[x])
        data_list_key.append(str(x+1))

    # logging.info(data_list)
    data_dict = {
        "results": dict(zip(data_list_key, data_list))
    }

    # logging.info(data_dict)
    json_convert = json.dumps(data_dict, indent=2, ensure_ascii=False)

    logging.info(json_convert)


    return func.HttpResponse(json_convert, status_code=200)
