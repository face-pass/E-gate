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
        images = req.files.getlist('image_file')
        csv_data = req.files.get('data_file')
        forms = req.form

        logging.info(images)
        logging.info(csv_data)

        # check empty request
        if not all([images, csv_data, forms]):
            logging.error("Error!! Please check request data")
            return func.HttpResponse("Bad request", status_code=400)            
        
        # check data file format    
        elif not csv_data.filename.endswith(".csv"):
            logging.error("Error!! Please check attandance data request!! -> data file has supported only 'csv' or 'xlsx' format")
            return func.HttpResponse("Bad data file request", status_code=400)

        logging.info("clear")

        # Connect Azure service
        blob = Blob()
        database = MySQL(forms['table'])
        logging.info("connected!!")

        # get register user name
        names = get_user(csv_data)

        logging.info(names)

    # check number of images data equal number of user name
        name_value = len(names)
        image_value = len(images)

        if name_value != image_value:
            # error response 
            logging.error("You must 'name_value' equal 'image_value' ")
            return func.HttpResponse("Error!! You must 'name_value' equal 'image_value'", status_code=400)

    # save image data to blob
        logging.info("started uploading image")
        blob.save_image_to_blob(images, forms['container'])

        logging.info("uploaded")

    # get image data url
        image_url = blob.get_image_url(forms['container'])

        logging.info(image_url)

    # Using register function

        logging.info("started registered")

        database.Register(names, image_url)

        logging.info("registered!!")
        return func.HttpResponse("Registerd user!", status_code=200)
    except:
        return func.HttpResponse("Internal Server Error", status_code=500)