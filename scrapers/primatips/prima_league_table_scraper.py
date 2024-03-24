from bs4 import BeautifulSoup


BASE_URL = "https:primatips.com"


import re


def scrape_league_table(req, league_data):

    TEAMS_DATA = []

    for data in league_data:

        league_url = data["primatips_table_url"]
        league_id = data["id"]
        league_name = data["name"]
        league_country = data["country"]

        response = req(league_url)
        if response is None:
            print('There is no response!\nQuitting...')
            return 
            
        soup = BeautifulSoup(response.text, "html.parser")

        league_table = soup.find("table", class_="standing")
        teams = league_table.find_all(class_="team")

        league_teams_info = []
        for team in teams:
            team_name = team.text.strip()
            team_url = team.find("a")["href"]

            league_teams_info.append({"team_name": team_name, "team_url": team_url})

            TEAMS_DATA.append(
                {
                    "primatips_name": team_name,
                    "primatips_url": f"{BASE_URL}{team_url}",
                    "league_id": league_id,
                    "league_name": league_name,
                    "league_country": league_country,
                }
            )

        return TEAMS_DATA
