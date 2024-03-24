from footystats.footy_league_stats_scraper import scrape_leagues_stats
from footystats.footy_league_table_scraper import scrape_tables
from footystats.footy_teams_scraper import scrape_teams_stats


def scraper(driver, **kwargs):
    if driver is None:
        return

    # leagues scraper function
    # footy_league_data = scrape_leagues_stats(driver)
    
    # table scraper function
    # league_data = kwargs.get('league_data')
    # footy_table_data = scrape_tables(driver, league_data)

    # teams scraper function
    teams_data = kwargs.get('teams_data')
    footy_teams_data = scrape_teams_stats(driver, teams_data)

    return footy_teams_data
