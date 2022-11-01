import logging
import azure.functions as func
from shared_code.DB import MySQL
from shared_code.azure_blob import Blob

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # get request
    try:
        json_data = req.get_json()
        table = json_data['table']
        request_ids = json_data['ids']
        container = json_data['container']

        # debug
        # logging.info(json_data)
        # logging.info(table)
        # logging.info(request_ids)

        if not table and request_ids and container:
            logging.error("Error!! Please check request!!")
            return func.HttpResponse("Bad request.", status_code=400)
        elif request_ids is not list:
            logging.error("Error!! `request_ids` must be list object")
            return func.HttpResponse("Bad request.", status_code=400)
        
        # connect Azure service
        blob = Blob(container)
        database = MySQL(table)

        # get image url
        image_url = database.getDBImage(request_ids)


        # delete blob from above result data
        blob.delete_image(image_url)

        # success flag
        logging.info("deleted image")

        # delete user name
        database.deleteUser(request_ids)

        return func.HttpResponse("Request Successed!!", status_code=200)

    except:
        return func.HttpResponse("Internal Server Error", status_code=500)