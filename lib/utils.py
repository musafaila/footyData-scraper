import requests
from requests.exceptions import (
    RequestException,
    Timeout,
    ConnectionError,
    HTTPError,
    InvalidURL,
    TooManyRedirects,
)
import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

import json
import os


def safeRequest(url, max_retries=3, retry_delay=2, timeout=10):
    retryable_exceptions = (Timeout, ConnectionError)

    for retry in range(max_retries + 1):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0"
            }
            response = requests.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response  # Successful response

        except HTTPError as e:
            print(f"HTTP error (Attempt {retry + 1}/{max_retries + 1}): {e}")
            return None  # HTTP errors are not retryable

        except InvalidURL as e:
            print(f"Inalid URL (Attempt {retry + 1}/{max_retries + 1}): {e}")
            return None  # invalid url error is not retryable

        except TooManyRedirects as e:
            print(f"Too many redirects (Attempt {retry + 1}/{max_retries + 1}): {e}")
            return None  # TooManyRedirects error is not retryable

        except RequestException as e:
            if isinstance(e, retryable_exceptions):
                if isinstance(e, Timeout):
                    print(
                        f"Request timeout (Attempt {retry + 1}/{max_retries + 1}): {e}"
                    )

                if isinstance(e, ConnectionError):
                    print(
                        f"Connection error (Attempt {retry + 1}/{max_retries + 1}): {e}"
                    )

                if retry < max_retries:
                    print(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    print("Max retries reached. Request failed.")
                    return None
            else:
                print("Request failed due to unknown error: ", e)


def initiate_driver(headless):
    firefox_options: Options = Options()

    if headless:        
        firefox_options.add_argument("-headless")

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
    with open(file_path, "r") as json_file:
        data = json.load(json_file)
        return data


def merge_json_files(directory, output_file):
    merged_data = []

    # Iterate over files in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            filepath = os.path.join(directory, filename)

            with open(filepath, "r") as file:
                data = json.load(file)
                # Merge data
                merged_data.extend(data)

    # Write merged data to output file
    with open(output_file, "w") as outfile:
        json.dump(merged_data, outfile, indent=4)


def stats_seperator(stats_data: []):
    overall_stats_list = []
    home_stats_list = []
    away_stats_list = []

    for data in stats_data:
        overall_stats_list.append(data["overall_stats"])
        home_stats_list.append(data["home_stats"])
        away_stats_list.append(data["away_stats"])

    save_to_json("merged_overall_stats.json", overall_stats_list)
    save_to_json("merged_home_stats.json", home_stats_list)
    save_to_json("merged_away_stats.json", away_stats_list)
