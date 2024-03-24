from bs4 import BeautifulSoup
import re

from selenium import webdriver

from footystats.urls import FOOTYSTATS_BASE_URL

def parse_table(page_source, league_id) -> {}:

    soup: BeautifulSoup = BeautifulSoup(page_source, "html.parser")

    league_table = soup.find(id="league-tables-wrapper").find(
        "table", class_="full-league-table"
    )
    league_table_body = league_table.find("tbody")
    league_table_rows = league_table_body.find_all("tr")

    TEAMS_STATS = []
    for row in league_table_rows:
        # position
        team_position: int = int(row.find("td", class_="position").text.strip())

        # team name
        team_name: str = row.find("td", class_="team").text.strip()

        # team url
        team_url: str = row.find("a")["href"]

        TEAMS_STATS.append(
            {
                "league_id": league_id,
                "position": team_position,
                "name": team_name,
                "footystats_url": f"{FOOTYSTATS_BASE_URL}{team_url}",
            }
        )

    return TEAMS_STATS


def scrape_tables(driver: webdriver, league_data: []):

    driver.get(FOOTYSTATS_BASE_URL)
    print(driver.title)
    return

    LEAUGE_DATA = []
    for data in league_data:
        try:
            league_url = data["footystats_table_url"]
            league_id = data["id"]
            # open a new tab
            driver.execute_script("window.open('');")
            # switch to the new tab
            driver.switch_to.window(driver.window_handles[1])

            # open the league url in the new tab
            driver.get(league_url)

            # get the page source
            page_source = driver.page_source

            # close the newly opened tab
            driver.close()
            # switch back to the old tab
            driver.switch_to.window(driver.window_handles[0])

            parsed_team_stats = parse_table(page_source, league_id)
            LEAUGE_DATA.append(parsed_team_stats)

        except Exception as err:
            print(f"Oops! could not scrape the url '{league_url}'.")
            print(err)
            continue

    return LEAUGE_DATA
