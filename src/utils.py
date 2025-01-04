"""Utility functions"""

import os
import json
from urllib.parse import urlsplit


def get_domain_name(url: str) -> str:
    """parse the news room neme from the website url, e.g. cnn, bbc"""
    domain = urlsplit(url).netloc
    if domain[-4:] in [".com", ".gov"]:
        return domain[:-4]

    if domain[-3:] in [".co", ".in"]:
        return domain[:-3]


def local_storage_path(domain_name: str) -> str:
    """Create local directory if not exists based to be used for storing the article locally

    Arguments:
        domain_name (str): Name of the local storage folder

    Returns:
        path of the created directory
    """

    storage_path = f"./{domain_name}"
    if not os.path.exists(storage_path):
        os.mkdir(storage_path)

    return storage_path


def clear_local_storage_path(domain_name: str) -> str:
    """Delete local storage if exists"""

    try:
        storage_path = f"./{domain_name}"
        if os.path.exists(storage_path):
            os.rmdir(storage_path)
        return True
    except Exception as e:
        return False


def create_document_file(storage_path: str, article_id: str, article_data: dict) -> str:
    """Store the article data in JSON format to local temp path"""

    article_file_name = f"{article_id}.json"
    article_file_path = os.path.join(storage_path, f"{article_file_name}.json")

    with open(article_file_path, "w") as fp:
        json.dump(article_data, fp)

    return article_file_path
