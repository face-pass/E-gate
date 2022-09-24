from azure.storage.blob import BlobServiceClient
import azure.functions as func

class Blob():

    def __init__(self):

        self.service_client = BlobServiceClient()


    def delete_image(self, url):

        