from scrapers.scraper import scraper
from parsers.parser import parser

from utils import make_request, initiate_driver
from db.supabase import save_data, initiate_client, fetch_data

import json


def main():
    # run all parsers here
    page_html = ""
    parser(page_html)

    # run all scrapers here
    with initiate_driver() as driver:
        if driver is None:
            print("Can't continue without a driver!!!")
            return

        league_data = ""
        with open("leagues_stats.json", "r") as f:
            league_data = json.load(f)

        return league_data[0:1]

        data = scraper(driver=driver, **{"league_data": league_data[0:1]})

        return data


# if "__name__" == "__main__":
data = main()

print(data)
