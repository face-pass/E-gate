import pandas as pd
import logging

def get_user_csv(data):

    # read csv file
    df = pd.read_csv(data)

    # debug
    logging.info(df)

    # get `name` column
    name = df.loc["dummy"]

    return name

def get_user_xlsx(data):

    # read xlsx file
    df = pd.read_excel(data)

    # debug
    logging.info()

    # find column `name`
    name = df.loc["dummy"]

    return name
