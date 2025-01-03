"""
Module: main.py
Created on: Dec 29, 2024
Last Modified on: Jan 02, 2025
Author: Amandeep Singh

Description:
    - Executes the main logic to scrape news articles using python

Argumennts:
    - newssite: link to the website from where news needs to be downloaded e.g. http://cnn.com
    - docs_count (default=0): if specified will only download the next n number of news articles


Dependencies:
    - Following are the dependencies for the program logic to execute
        - Service Principle which should have following roles
            - Storage Object Principal
            - Cloud Datastore Owner

        - Existing cloud storage bucket to upload the news articles
        - Firestore databse to create the collection
        - Set the following environment variables
            - NEWS_BUCKET=<gcp-storage-bucket-name> to upload the articles
            - DATABASE_NAME=<firestore databse name>
            - COLLECTION_NAME=<collection name>
            - GOOGLE_APPLICATION_CREDENTIALS=<path-to-the-service-principal-credentials.json>

"""

import os
import argparse
import logging
from dotenv import load_dotenv
from src.get_articles import download_articles

import functions_framework

def main(news_site: str, num_of_docs: int=0) -> None:
    logging.info("Starting proccess...")

    if len(news_site) == 0:
        logging.info("Must provide the url for the news website!")
        return None

    msg = download_articles(news_site=news_site, num_of_docs=num_of_docs)

    return msg

@functions_framework.http
def get_website_articles(request): 
    if request.args:
        docs_count = request.args.get('docs_count')
        newssite = request.args.get('newssite') 
    elif request.get_json():
        request_json = request.get_json()
        docs_count = request_json['docs_count']
        newssite = request_json['newssite']
    elif request.values:
        request_data = request.values
        docs_count = request_data['docs_count']
        newssite = request_data['newssite']
    else:
        return f"Must specify newsite and docs count"

    msg = download_articles(news_site=newssite, num_of_docs=int(docs_count))

    return msg

if __name__ == "__main__":

    logging.basicConfig(
        format="{asctime} - {levelname} - {message}", 
        style="{", 
        datefmt="%Y-%m-%d %H:%M",
        level=logging.DEBUG,
    )

    load_dotenv()
    parser = argparse.ArgumentParser(prog='news-downloader')
    parser.add_argument('--newssite', help='Website link from where news to be downloaded', default="")
    parser.add_argument('--docs_count', help='Number of docs to fetch', type=int,  default=0)
    args = parser.parse_args()
    msg = main(args.newssite, args.docs_count)
    print(msg)
