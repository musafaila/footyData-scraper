from bs4 import BeautifulSoup
import re

from selenium import webdriver


FOOTYSTATS_BASE_URL = "https://footystats.org"


def scrape_team_info(driver: webdriver) -> {}:
    # open a new tab
    driver.execute_script("window.open('');")
    # switch to the new tab
    driver.switch_to.window(driver.window_handles[1])

    # open the league url in the new tab
    driver.get(f"{FOOTYSTATS_BASE_URL}{league_url}")
    return {'title': driver.title}

    # wait = WebDriverWait(driver, 10)
    # wait.until(EC.title_contains(""))
    # time.sleep(30)

    page_content = driver.page_source
    # close the newly opened tab
    driver.close()
    # switch back to the old tab
    driver.switch_to.window(driver.window_handles[0])

    soup: BeautifulSoup = BeautifulSoup(page_content, "html.parser")

    league_name: str = soup.find("h1", class_="leagueName").text.strip()
    league_name: str = re.match(r"(.+?) Table & Stats", league_name).group(1)

    league_details_container = soup.find(class_="league-details")
    details = league_details_container.find_all(class_="detail")

    def find_detail(text: str) -> str or int:
        for detail in details:
            caption = detail.find(class_="w35")
            if caption.text.strip().lower() == text.lower():
                return detail.find(class_="w65").text.strip()

    leauge_country: str = find_detail("nation")

    leauge_division: str = find_detail("division")

    leauge_num_of_teams: int = find_detail("teams")

    return {
        "name": league_name,
        "country": leauge_country,
        "division": leauge_division,
        "num_of_teams": leauge_num_of_teams,
        "footystats_table_url": f"{FOOTYSTATS_BASE_URL}{league_url}",
    }


def teams_scraper(driver: webdriver, league_data: []):
    if driver is None:
        return

    driver.get(FOOTYSTATS_BASE_URL)

    LEAGUE_URLS = [league_data["footystats_table_url"] for data in data]

    LEAUGE_DATA = []
    for url in LEAGUE_URLS:
        try:
            data = scrape_team_info(driver, url)
            print(data)
            LEAUGE_DATA.append(data)
        except Exception as err:
            print(f"Oops! could not scrape the url '{url}'.")
            print(err)
            continue

    return LEAUGE_DATA
