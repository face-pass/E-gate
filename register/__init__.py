import logging

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # connect Azure service

    # get request form data


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
