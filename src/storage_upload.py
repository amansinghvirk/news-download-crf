"""
Module: storage_upload.py
Created on: Dec 29, 2024
Last Modified on: Jan 02, 2025
Author: Amandeep Singh

Description:
    - connects to the gcp cloud storage
    - upload the file to the bucket

"""
import os
import logging
from google.cloud import storage


# define function that uploads a file from the bucket
def upload_news_article(
    source_file_name: str, 
    destination_file_name: str
) -> bool: 
    """Upload file to the GCP cloud storage bucket"""
    try:
        bucket_name = os.environ["NEWS_BUCKET"]
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_file_name)
        blob.upload_from_filename(source_file_name)
        logging.info(f"Article uploaded to {bucket_name}/{destination_file_name}")

        return True
    except Exception as e:
        logging.error(e)
    
    return False