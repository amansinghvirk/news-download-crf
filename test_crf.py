"""
Module: test_crf.py
Created on: Jan 03 , 2025
Last Modified on: Jan 02, 2025
Author: Amandeep Singh

Description:
    - Test the cloud run url by passing predefined data 
    - validates cloud run function running 
        - locally
        - deployed as unauthenticated function
        - deployed as authenticated function using credentials passed for the 
            service principal which has permissions to invoke the function

"""

import argparse
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession


TEST_DATA = {"newssite": "https://finance.yahoo.com", "docs_count": "5"}

def main(url, key_file=None):
    """test the cloud run function url by trigger function using http-trigger"""

    

    if key_file:
        creds = service_account.IDTokenCredentials.from_service_account_file(
            key_file, target_audience=url
        )

        authed_session = AuthorizedSession(creds)

        # make authenticated request and print the response, status_code
        response = authed_session.post(url, json=TEST_DATA, timeout=100)

    else:
        response = requests.post(url, json=TEST_DATA, timeout=100)

    if response.status_code == 200:
        print(response.content)
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        if response.status_code:
            print("Provide the valid credentials to access the function URL")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="news-downloader")
    parser.add_argument("--crf_url", help="URL of cloud run function", default="")
    parser.add_argument(
        "--key_file",
        help="Path to the credentials file for the invoker service principal",
        default="",
    )
    args = parser.parse_args()
    main(url=args.crf_url, key_file=args.key_file)
