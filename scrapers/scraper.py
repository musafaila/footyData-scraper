from scraper.footy_league_scraper import scrape_all_leagues
from scraper.footy_teams_scraper import teams_scraper


def scraper(driver, **kwargs):
    if driver is None:
        return

    footy_leagues_data = scrape_all_leagues(driver)


    return footy_teams_data
