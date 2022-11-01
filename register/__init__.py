import logging
import azure.functions as func
import cv2
from shared_code.DB import MySQL
from shared_code.azure_blob import Blob
from shared_code.user_function import get_user

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # get request form data
    try:
        method = req.method
        file = req.files
        forms = req.form

        # debug
        logging.info(file)
        # logging.info(forms)
        # logging.info(all([file, forms]))
        

        # check empty request
        if not all([file, forms]):
            logging.error("Error!! Please check request data")
            return func.HttpResponse("Bad request", status_code=400)            

        # check image file format
        elif all([file['image_file'].filename.endswith(".jpg"), file['image_file'].filename.endswith(".png")]):
            logging.error("Error!! Please check image file format!! -> image file has supported only 'jpg' or 'png' format")
            return func.HttpResponse("Bad image file request", status_code=400)

        # check data file format    
        elif all([file['data_file'].filename.endswith(".csv"), file['data_file'].filename.endswith(".xlsx")]):
            logging.error("Error!! Please check attandance data request!! -> data file has supported only 'csv' or 'xlsx' format")
            return func.HttpResponse("Bad data file request", status_code=400)

        # Connect Azure service
        blob = Blob(forms['container'])
        # database = MySQL(forms['table'])

        # get register user name
        names = get_user(file)

    # check number of image data equal number of user name
        name_value = len(names)
        image_value = len(file.getlist('image_file'))

        if name_value != image_value:
            # error response 
            logging.error("You must 'name_value' equal 'image_value' ")
            return func.HttpResponse("Bad request. You must 'name_value' equal 'image_value'", status_code=400)

    # save image data to blob
        blob.save_image_to_blob(file['image_file'])

    # get image data url
        image_url = blob.get_image_url()

        logging.info(image_url)

    # Using register function
        # for name in names:
        #     database.Register(image_url, name)

        return func.HttpResponse("Registerd user!", status_code=200)
    except :
        return func.HttpResponse("Internal Server Error", status_code=500)