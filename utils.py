import requests
from tenacity import retry, stop_after_attempt, wait_fixed

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

import json


@retry(stop=stop_after_attempt(5), wait=wait_fixed(1))
def make_request(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0"
    }

    try:
        response = requests.get(
            url, headers=headers, timeout=5
        )  # Set max timeout to 5 seconds
        response.raise_for_status()  # Raise HTTPError for bad status codes
        return response
    except requests.exceptions.RequestException as err:
        print(f"Failed to request the url {url}!")
        print(err)


def initiate_driver():
    firefox_options: Options = Options()
    # firefox_options.add_argument("-headless")

    try:
        driver = webdriver.Firefox(options=firefox_options)
        return driver
    except Exception as err:
        print("Driver initiation failed!")
        print(err)


def save_to_json(file_path, data):
    with open(file_path, "w") as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)


def load_json(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        return data