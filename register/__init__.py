import logging
import azure.functions as func
from shared_code.DB import MySQL
from shared_code.azure_blob import Blob

# Connect Azure service
blob = Blob()
database = MySQL()


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # get request form data
    try:
        image_file = req.files
        data_file = req.files
        table = req.params.get("table")


        # debug
        logging.info(image_file)
        logging.info(data_file)
        logging.info(table)

        if not image_file and data_file and table:
            logging.error("Error!! Please check request data")
            return func.HttpResponse("Bad request", status_code=400)

            



    # check request form data and file format


    # check csv or xlsx file


        # request data format == csv

        # request data format == xlsx


    # check number of image data equal number of user name


        # error response 


    # ---- loop ----

        # save image data to blob


        # get image data url



    # Using register function
