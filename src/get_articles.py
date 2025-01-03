"""
Module: news_download.py
Created on: Dec 29, 2024
Last Modified on: Jan 02, 2025
Author: Amandeep Singh

Description:
    - provides function download_articles() with following functionality
        - extract the domain name from the url provided e.g. cnn from www://cnn.com
        - connect to gcp firestore database, and get the url list for the downloaded artiles
            for the domain
        - search the news website for the posts and compare with downloaded article urls,
            if there are any news articles available
        - download the not downloaded articles
        - save the article in json form in temp directory, upload the document to GCP cloud storage
            and delete the temp file
        - add the item to the firestore collections

"""

import os
import logging
from uuid import uuid4
from newspaper import build, parsers,  Article

from .firestore_db import get_registered_articles, create_item
from .utils import get_domain_name, local_storage_path, create_document_file, clear_local_storage_path
from .storage_upload import upload_news_article

def download_articles(news_site: str, num_of_docs: int=0):
    """Download articles from the url of given site
    Arguments:
        news_site (str): URL of the site from which articles need to be extracted
            e.g. http://cnn.com, http://bbc.com
        num_of_docs (int) default=0: Number of articles need to be parsed in execution

    Return:


    """

    article_dict = dict()
    local_temp_storage = "temp"

    domain_name = get_domain_name(news_site)
    storage_path = local_storage_path(domain_name=local_temp_storage)

    papers = get_papers(news_site)
    urls_to_download = get_new_article_urls(papers, domain_name)

    if num_of_docs > 0: 
         urls_to_download = urls_to_download[:num_of_docs]
        
    n_parsed = 0
    for url in urls_to_download:

        article = parse_article(url)

        if article:

            # format to dictionary
            article_data = _create_document(
                domain_name,
                article
            )

            # create json document
            article_id =  uuid4().hex
            article_file_path = create_document_file(
                storage_path=storage_path,
                article_id=article_id, 
                article_data=article_dict
            )

            # upload to cloud storage
            upload_news_article(
                source_file_name=article_file_path,
                destination_file_name=f'{domain_name}/{article_id}.json'
            )

            # save to firestore databse
            is_item_saved=create_item(
                doc_id=article_id, 
                data=article_data
            )

            if is_item_saved:
                logging.info("Arcticle id saved to db.")
            else:
                logging.info("Error in saving url to db.")

            # Delete from local storage
            os.remove(article_file_path)

            n_parsed += 1

    if not clear_local_storage_path(local_temp_storage):
        print("Error cleaning local temp storage!")

    return f"{n_parsed} articles parsed form {news_site} and saved to cloud storage!" 

def get_papers(news_site: str):
     """Set parser for news site"""
     papers = build(news_site, memoize_articles=False)

     return papers

def get_new_article_urls(papers: parsers, domain_name: str) -> tuple:
    """Compare the parser urls with urls in registered database 
    - Return new URLs
    """

    registerd_articles = get_registered_articles(domain_name=domain_name)

    urls_to_download = [
         article.url for article in papers.articles 
         if article.url not in registerd_articles
    ]

    return urls_to_download

def parse_article(url: str) -> Article:
    """Parse article from the given URL"""

    try:
        article = Article(url)
        article.download()
        article.parse()
        return article
    except Exception as e:
        logging.error("Error in parsing article...")
        logging.error(e)
        return None
    
def _create_document(
    domain_name: str, 
    article: Article
) -> dict:

    article_data={
        'domain': domain_name,
        'url': article.url,
        'title': article.title,
        'text': article.text
    }

    return article_data