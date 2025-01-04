"""
Module: firestore_db.py
Created on: Dec 29, 2024
Last Modified on: Jan 02, 2025
Author: Amandeep Singh

Description:
    - connections to the firestore database using firestore client
    - creates collection if not exist
    - add document to the collection
    - add items to the document
"""

import os
import logging
from google.cloud.firestore import Client
from google.cloud.firestore_v1.base_query import FieldFilter


def get_firestore_client() -> Client:
    """Initialize the firestore clinet"""
    try:
        return Client(database=os.environ["DATABASE_NAME"])
    except Exception as e:
        logging.error("Error connecting to the databse")
        return None


def create_item(doc_id: str, data: dict) -> bool:
    """Add article to the collection"""
    try:
        db = get_firestore_client()
        doc_ref = db.collection(os.environ["COLLECTION_NAME"]).document(doc_id)
        doc_ref.set(data)

        return True
    except Exception as e:
        logging.error(e)
        return False


def get_registered_articles(domain_name: str) -> list:
    """Returns the list of urls for the specified domain from the downloaded articles"""

    try:
        db = get_firestore_client()
        docs = (
            db.collection(os.environ["COLLECTION_NAME"])
            .where(filter=FieldFilter("domain", "==", domain_name))
            .stream()
        )

        registerd_articles = []
        for doc in docs:
            registerd_articles.append(doc.to_dict().get("url"))
        return registerd_articles

    except Exception as e:
        logging.error("Error fetching the articles list")
        raise e
