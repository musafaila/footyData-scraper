from bs4 import BeautifulSoup


def scrape_primatips_league_stats(page_html):

    if page_html == "":
        return

    soup = BeautifulSoup(page_html, "html.parser")

    stats_wrapper = soup.find(id="statistic-wrapper")

    season = stats_wrapper.find(class_="seasons-select").text.strip().split(":")[-1]

    all_stats_cells = stats_wrapper.find(class_="league-stat-main").find_all("td")
    # return all_stats_cells

    def find_cell(text: str) -> str:
        for cell in all_stats_cells:
            if cell.text.strip().lower() == text.lower():
                data = cell.find_next(class_="data").text.strip()
                return data

    num_of_matches = int(find_cell("matches"))

    matches_played = int(find_cell("Played"))

    progress = round((matches_played / num_of_matches) * 100, 0)

    avg_goals = float(find_cell("Average"))

    return {
        "season": season,
        "num_of_matches": num_of_matches,
        "matches_played": matches_played,
        "progress": progress,
        "avg_goals": avg_goals
    }
