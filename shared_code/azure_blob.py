import azure.functions as func
import logging
from azure.storage.blob import BlobServiceClient
from azure.storage.blob import ContentSettings, ContainerClient
from config import blob_config

class Blob():

    def __init__(self, container):
        self.service_client = BlobServiceClient.from_connection_string(blob_config)
        self.container_client = self.service_client.get_container_client(container)
        self.blob_client = self.service_client.get_blob_client(container)

    def save_image_to_blob(self, images):
        image_content_setting = ContentSettings(content_type='image/jpeg')

        for image in images:
            with open(image, "rb") as data:
                self.blob_client.upload_blob(data, overwrite=True, content_settings=image_content_setting)

    def get_image_url(self):
       blob_list = self.container_client.list_blobs()

       # debug
       logging.info(blob_list)

       return blob_list

    def delete_image(self, url):
        self.container_client.delete_blobs(url)

        