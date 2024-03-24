# from scrapers.footystats.footystats import scraper as footystats_scraper
from scrapers.primatips.scraper import primatips_scraper 

# from scrapers.flashscore.flashscore import add_flash_urls

from utils import (
    safeRequest,
    initiate_driver,
    save_to_json,
    load_json,
    merge_json_files,
)
from lib.add_urls import add_teams_urls
from db.supabase import save_data, initiate_client, fetch_data


def main():

    for i in range(10, 37):
        league_index: int = i

        # Teams data that will represent the teamA data point
        teams_data = load_json("data/teams.json")
        # Leagues DB data that will represent the teamB data point
        leagues_db_data = load_json("data/leagues_DB_records.json")

        add_teams_urls(
            teams_data,  # Json file 1
            leagues_db_data,  # Json file 2
            league_index=league_index,
            **{
                "scraping_func": primatips_scraper,
                "req": safeRequest,
                "driver": None,
                "save_to_json": save_to_json,
            }
        )

    # NOTE: THIS SPACE IS FOR FOOTYSTATS SCRAPERS!
    # run all scrapers here
    # with initiate_driver() as driver:
    #     if driver is None:
    #         print("Can't continue without a driver!!!")
    #         return

    #     data = footystats_scraper(driver=driver, **{"teams_data": teams_data})

    #     save_to_json("data/isr_turk_grc_teams_stats.json", data)

    #     [print(d) for d in data]


main()
