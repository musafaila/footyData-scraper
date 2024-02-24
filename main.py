from scrapers.scraper import scraper
from parsers.parser import parser

from utils import make_request, initiate_driver, save_to_json, load_json
from db.supabase import save_data, initiate_client, fetch_data


def main():
    # run all parsers here
    page_html = ""
    parser(page_html)

    # run all scrapers here
    all_teams_data = load_json("data/footy_teams_urls.json")

    teams_data = []
    for data in all_teams_data:
        if data["country"] == "England":
            for team in data["teams"]:
                teams_data.append(team)

    with initiate_driver() as driver:
        if driver is None:
            print("Can't continue without a driver!!!")
            return

        data = scraper(driver=driver, **{"teams_data": teams_data[0:1]})

        print(data)


# if "__name__" == "__main__":
main()
