import os
import argparse
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession

def main(url, key_file=None):

    test_data = {'newssite': 'http://cnn.com', 'docs_count': '5'}


    if key_file:
        creds = service_account.IDTokenCredentials.from_service_account_file(
            key_file, 
            target_audience=url
        )

        authed_session = AuthorizedSession(creds)

        # make authenticated request and print the response, status_code
        response = authed_session.post(url, json=test_data)  
    
    else:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, json=test_data)

    if response.status_code == 200:
        print(response.content)
    else:
        print(f'Failed to retrieve the page. Status code: {response.status_code}')
        if response.status_code:
            print(f"Provide the valid credentials to access the function URL")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='news-downloader')
    parser.add_argument('--crf_url', help='URL of cloud run function', default="")
    parser.add_argument('--key_file', help='Path to the credentials file for the invoker service principal', default="")
    args = parser.parse_args()
    main(url=args.crf_url, key_file=args.key_file)