import logging
import azure.functions as func
import cv2
from shared_code.DB import MySQL
from shared_code.azure_blob import Blob
from shared_code.user_function import get_user_csv, get_user_xlsx

# Connect Azure service
blob = Blob()
database = MySQL()

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # get request form data
    try:
        method = req.method
        image_file = req.files
        data_file = req.files
        table = req.params.get("table")

        # debug
        logging.info(image_file)
        logging.info(data_file)
        logging.info(table)

        # check request form data and file format
        if not image_file and data_file and table:
            logging.error("Error!! Please check request data")
            return func.HttpResponse("Bad request", status_code=400)            
        elif not image_file.endswith(".jpg") or image_file.endswith(".png"):
            logging.error("Error!! Please check image file format!! -> image file has supported only 'jpg' or 'png' format")
            return func.HttpResponse("Bad image file request", status_code=400)
        elif not data_file.endswith(".csv") or data_file.endswith(".xlsx"):
            logging.error("Error!! Please check attandance data request!! -> data file has supported only 'csv' or 'xlsx' format")
            return func.HttpResponse("Bad data file request", status_code=400)

    # check csv or xlsx file

        if data_file.endswith(".csv"):
            names = get_user_csv(data_file)
        else:
            data_file.endswith(".xlsx")
            names = get_user_xlsx(data_file)

    # check number of image data equal number of user name
        name_value = len(name)
        image_value = len(image_file)   

        if name_value != image_value:
            # error response 
            logging.error("You must 'name_value' equal 'image_value' ")
            return func.HttpResponse("Bad request. You must 'name_value' equal 'image_value'", status_code=400)

    # save image data to blob
        blob.save_image_to_blob(image_file)

    # get image data url
        image_url = blob.get_image_url()

    # Using register function
        for name in names:
            database.Register(image_url, name)

        return func.HttpResponse("Registerd user!", status_code=200)
    except:
        return func.HttpResponse("Internal Server Error", status_code=500)