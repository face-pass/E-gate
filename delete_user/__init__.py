import logging
import azure.functions as func
from shared_code.DB import MySQL
from shared_code.azure_blob import Blob

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    file_name = []

    # get request
    try:
        json_data = req.get_json()
        table = json_data['table']
        request_ids = json_data['ids']
        container = json_data['container']

        if not table and request_ids and container:
            logging.error("Error!! Please check request!!")
            return func.HttpResponse("Bad request.", status_code=400)
        elif not type(request_ids) == list:
            logging.error("Error!! `request_ids` must be list object")
            return func.HttpResponse("Bad request.", status_code=400)
              
        # connect Azure service
        blob = Blob()
        database = MySQL(table)

        # get delete image url
        image_urls = database.getDBImage(request_ids)

        # get image file name from image_url
        for image_url in image_urls:
            split_url = image_url.split("/")
            file_name.append(split_url[-1])

        # # delete blob from above result data
        blob.delete_image(container, file_name, request_ids)

        # # delete user name
        database.DeleteUser(request_ids)

        return func.HttpResponse("Request Successed!!", status_code=200)

    except:
        return func.HttpResponse("Internal Server Error", status_code=500)