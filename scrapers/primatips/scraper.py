from scrapers.primatips.prima_league_stats_scraper import scrape_primatips_league_stats
# from primatips.prima_teams_scraper import scrape_team_stats
from scrapers.primatips.prima_league_table_scraper import scrape_league_table


def primatips_scraper(req, **kwargs):
    if req is None:
        return

    # data = parse_primatips_league_stats(page_html)

    # data = parse_team_stats()

    league_data = kwargs.get("league_data")
    data = scrape_league_table(req, league_data)

    return data