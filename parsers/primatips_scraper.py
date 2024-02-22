import requests
from bs4 import BeautifulSoup

PRIMATIPS_BASE_URL = "https://primatips.com"

def scrape_league_table(league_url):
    response = requests.get(f"{BASE_URL}/{league_url}")
    soup = BeautifulSoup(response.text, "html.parser")

    league_table = soup.find("table", class_="standing")
    teams = league_table.find_all(class_="team")
    teams_links_and_names = []
    for team in teams:
        team_name = team.text.strip()
        team_link = team.find("a")["href"]
        teams_links_and_names.append({"team_name": team_name, "team_link": team_link})

    teams_stats = []
    for team_info in teams_links_and_names:
        overall_stats = scrape_team_stats(team_info["team_link"])
        home_stats = scrape_team_stats(team_info["team_link"], type="home")
        away_stats = scrape_team_stats(team_info["team_link"], type="away")

        teams_stats.append(
            {
                "name": team_info["team_name"],
                "overall_stats": overall_stats,
                "home_stats": home_stats,
                "away_stats": away_stats,
            }
        )

    return teams_stats


def scrape_team_stats(team_link, type="overall"):
    if type == "overall":
        url_to_scrape = f"{BASE_URL}{team_link}"
    if type == "home":
        url_to_scrape = f"{BASE_URL}{team_link}/league-home"
    if type == "away":
        url_to_scrape = f"{BASE_URL}{team_link}/league-away"

    # response = requests.get(f"{BASE_URL}{teams_links[0]}")
    response = requests.get(url_to_scrape)
    soup = BeautifulSoup(response.text, "html.parser")

    stats_table_identifier = soup.find(
        lambda tag: tag.name == "h2" and "Team Statistic" in tag.text
    )
    stats_table = stats_table_identifier.find_next("table")

    matches_played = int(
        soup.find("td", class_="caption", string="Matches").find_next("td").text
    )
    goals_scored = int(
        soup.find("td", class_="caption", string="Goals For").find_next("td").text
    )
    goals_conceded = int(
        soup.find("td", class_="caption", string="Goals Against").find_next("td").text
    )
    gsr = round((goals_scored / matches_played), 2)
    gcr = round((goals_conceded / matches_played), 2)

    clean_sheets = matches_played - int(
        soup.find("td", class_="caption", string="Matches Conceded")
        .find_next("td")
        .text
    )

    fts = matches_played - int(
        soup.find("td", class_="caption", string="Matches Scored").find_next("td").text
    )

    avg_goals = round((gsr + gcr), 2)

    stats = {
        "matches_played": matches_played,
        "goals_scored": goals_scored,
        "goals_conceded": goals_conceded,
        "gsr": gsr,
        "gcr": gcr,
        "clean_sheets": clean_sheets,
        "fts": fts,
        "avg_goals": avg_goals,
    }

    return stats


all_leagues_data = []
for league_name, league_url in LEAGUE_URLS.items():
    try:
        print(f"scraping data for {league_name}...")
        league_data = scrape_league_table(league_url)
        all_leagues_data.append({league_name: league_data})
        print(f"{league_name}'s data scraped succesfully!")
    except Exception as e:
        print(f"Error scraping data for the league {league_name}: {e}")
        
        
print(all_leagues_data)