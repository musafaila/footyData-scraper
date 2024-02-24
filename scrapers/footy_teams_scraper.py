from selenium import webdriver
from bs4 import BeautifulSoup

from scrapers.urls import FOOTYSTATS_BASE_URL


def parse_team_stats(page_source):
    soup = BeautifulSoup(page_source, "html.parser")
    team_stats = {"title": soup.title}

    identifiers = soup.find_all("h2", class_="section-title")

    def find_stat_rows(caption: str) -> []:
        for identifier in identifiers:
            if caption.lower() in identifier.text.strip().lower():
                stat_rows = (
                    identifier.find_parent(class_="stat-group")
                    .find("table")
                    .find("tbody")
                    .find_all("tr")
                )
                return stat_rows

    def find_stat(caption: str, stat_rows: [], num=False) -> str:
        for row in stat_rows:
            key = row.find("td", class_="key")
            if key.text.strip().lower() == caption.lower():
                stats_cells = key.find_siblings("td")

                if num:
                    return [float(stat_cell.text.strip()) for stat_cell in stats_cells]

                return [stat_cell.text.strip() for stat_cell in stats_cells]

    goals_conc_rows = find_stat_rows("Goals Conceded")

    gcr_ovrll = find_stat("Conceded / Match", goals_conc_rows, num=True)[0]
    gcr_home = find_stat("Conceded / Match", goals_conc_rows, num=True)[1]
    gcr_away = find_stat("Conceded / Match", goals_conc_rows, num=True)[-1]

    return {
        "overall_stats": {"gcr_overall": gcr_ovrll},
        "home_stats": {"gcr_home": gcr_home},
        "away_stats": {"gcr_away": gcr_away},
    }


def scrape_teams_stats(driver: webdriver, teams_data: []):
    TEAMS_STATS = []
    for data in teams_data:
        try:
            team_url = data["footystats_url"]
            team_id = data["id"]
            # open a new tab
            driver.execute_script("window.open('');")
            # switch to the new tab
            driver.switch_to.window(driver.window_handles[1])

            # open the league url in the new tab
            driver.get(team_url)

            # get the page source
            page_source = driver.page_source

            # close the newly opened tab
            driver.close()
            # switch back to the old tab
            driver.switch_to.window(driver.window_handles[0])

            parsed_team_stats = parse_team_stats(page_source)
            TEAMS_STATS.append(parsed_team_stats)

        except Exception as err:
            print(f"Oops! could not scrape the url '{team_url}'.")
            print(err)
            continue

    return TEAMS_STATS


""" Todo: Scraped Teams:
        - England teams
"""
