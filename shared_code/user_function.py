import pandas as pd
import logging
import azure.functions as func
from io import StringIO

def get_user(data):

    # df = pd.read_csv(data["data_file"])
    # logging.info(df)


    try:
        # read csv file
        df = pd.read_csv(data["data_file"])

        logging.info(df)

        names = df["name"].values.tolist()

        return names
    except FileNotFoundError as e:
        
        logging.error(e)
