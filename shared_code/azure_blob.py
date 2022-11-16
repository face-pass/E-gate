import azure.functions as func
import logging
from azure.storage.blob import BlobServiceClient
from azure.storage.blob import ContentSettings, ContainerClient
# from config import blob_config
from shared_code.hide_config import blob_config

class Blob():

    def __init__(self):
        self.service_client = BlobServiceClient.from_connection_string(blob_config)

    def save_image_to_blob(self, images, container):

        logging.info(container)
        blob_client = self.service_client.get_blob_client(container=container, blob=images.filename)
        logging.info("uploading image...")
        
        blob_client.upload_blob(images, overwrite=True)

    def get_image_url(self, container):
        image_url = []
        container_client = self.service_client.get_container_client(container=container)
        blob_list = container_client.list_blobs()

        # debug
        logging.info(blob_list)
        for blob in blob_list:
                blob_name = blob.name
                image_url.append(f"https://egate12.blob.core.windows.net/db-image/{blob_name}")

        return image_url

    def delete_image(self, container, file_names, delete_ids):

        logging.info(file_names)

        # blob_client = self.service_client.get_blob_client(container=container)
        container_client = self.service_client.get_container_client(container=container)

        for delete_id in delete_ids:
            container_client.delete_blobfile_names[delete_ids-1]
            