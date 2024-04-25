from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

import time


BASE_URL = "https://www.flashscore.com/"

def parse_league_table(page_source, league_id, league_name, league_country):
    league_teams_data = []
    soup = BeautifulSoup(page_source, "html.parser")

    league_table = soup.find("div", id="tournament-table").find("div", class_="ui-table")        
    league_table_body = league_table.find("div", class_="ui-table__body")
    league_table_rows = league_table_body.find_all("div", "ui-table__row")


    for row in league_table_rows:
        team_name = row.find("a", class_="tableCellParticipant__name").text.strip()
        team_url = row.find("a", class_="tableCellParticipant__name")["href"]
        team_position = int(row.find("div", class_="tableCellRank").text.strip())

        team_data = {
            "flashscore_name": team_name,
            "flashscore_url": f"{BASE_URL}{team_url}",
            "league_id": league_id,
            "league_name": league_name,
            "league_country": league_country,    
        }

        league_teams_data.append(team_data)


    return league_teams_data


def scrape_league_table(driver, league_data):

    if driver is None:
        print("There is no driver!\nQuitting...")
        return

    TEAMS_DATA = []

    for data in league_data:

        try:

            league_table_url = data["flashscore_table_url"]
            league_id = data["id"]
            league_name = data["name"]
            league_country = data["country"]

            driver.execute_script("window.open('');")
            # switch to the new tab
            driver.switch_to.window(driver.window_handles[1])

            driver.get(league_table_url)

            time.sleep(5)

            try:
                # click the accept button if availabe
                # one_trust_container = driver.find_element(By.ID, "onetrust-group-container")
                one_trust_button = driver.find_element(By.ID, "onetrust-accept-btn-handler")
                one_trust_button.click()
            except Exception as error:
                # print(error)
                print(f"One Trust Button Not Found for {league_name}!")
                pass

            page_source = driver.page_source

            team_data = None
            try:
                team_data = parse_league_table(page_source, league_id, league_name, league_country)
            except Exception as error:
                print(error)
                pass

            if team_data is not None:
                TEAMS_DATA.extend(team_data)

            
            # close the newly opened tab
            driver.close()
            # switch back to the old tab
            driver.switch_to.window(driver.window_handles[0])
        except Exception as error:
            print(error)
            continue
    
        
    return TEAMS_DATA
