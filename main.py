# from scrapers.footystats.footystats import scraper as footystats_scraper
from scrapers.primatips.scraper import primatips_scraper
from scrapers.flashscore.table_scraper import scrape_league_table as scrape_flash_table


from lib.utils import (
    safeRequest,
    initiate_driver,
    save_to_json,
    load_json,
    merge_json_files,
)
from lib.add_teams_urls import add_site_urls
from db.supabase import save_data, initiate_client, fetch_data


# from playwright.sync_api import sync_playwright

def main():

    scraped_teams_data = load_json("data/flash_team_name.json")
    teams_db_data = load_json("data/teams.json")
    leagues_db_data = load_json("data/leagues_DB_records.json")

    add_site_urls(scraped_teams_data, teams_db_data, leagues_db_data)


    # with sync_playwright() as p:
    #     browser = p.chromium.launch()
    #     page = browser.new_page()
    #     page.goto("https://www.flashscore.com/")
    #     page

    # with initiate_driver(headless=False) as driver:    

    #     league_data = load_json("data/leagues_DB_records.json")

    #     scraped_data = scrape_flash_table(driver, league_data)

    #     save_to_json("data/flash_team_name.json", scraped_data)

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
