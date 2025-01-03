import os
import argparse
import requests

def main(url):
    param = {'newssite': 'http://cnn.com', 'docs_count': '5'}

    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, json=param)

    if response.status_code == 200:
        print(response.content)
    else:
        print(f'Failed to retrieve the page. Status code: {response.status_code}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='news-downloader')
    parser.add_argument('--crf_url', help='URL of cloud run function', default="")
    args = parser.parse_args()
    main(url=args.crf_url)