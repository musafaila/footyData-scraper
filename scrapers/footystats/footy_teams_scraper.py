from selenium import webdriver
from bs4 import BeautifulSoup


def find_stat_rows(caption: str, identifiers: []) -> []:
    for identifier in identifiers:
        if caption.lower() in identifier.text.strip().lower():
            stat_tables = identifier.find_parent("section").find_all("tbody")
            stat_rows = []
            for table in stat_tables:
                rows = table.find_all("tr")
                for row in rows:
                    stat_rows.append(row)
            return stat_rows


def find_stat(caption: str, stat_rows: [], num=False) -> []:
    for row in stat_rows:
        key = row.find("td", class_="key")
        if key.text.strip().lower() == caption.lower():
            stats_cells = key.find_next_siblings("td")

            if num:
                stats = [
                    float(stat_cell.text.strip().replace("%", ""))
                    for stat_cell in stats_cells
                ]
                return stats

            stats = [stat_cell.text.strip() for stat_cell in stats_cells]
            return stats


def calc_conv_rate_ontarget(gsr, sot):
    cr_list = []
    for i in range(3):
        if sot[i] == 0:
            cr_ont = 0
        else:
            cr_ont = round((gsr[i] / sot[i]) * 100, 1)

        cr_list.append(cr_ont)

    return cr_list


def clean_stats(stats: {}, team_id: str) -> {}:
    overall_stats = {}
    home_stats = {}
    away_stats = {}

    for key, val in stats.items():
        overall_stats[key] = val[0]
        home_stats[key] = val[1]
        away_stats[key] = val[-1]

    return {
        "overall_stats": {"team_id": team_id, **overall_stats},
        "home_stats": {"team_id": team_id, **home_stats},
        "away_stats": {"team_id": team_id, **away_stats},
    }


def parse_team_stats(page_source, team_id: str):
    soup = BeautifulSoup(page_source, "html.parser")

    # locators identifiers
    identifiers = soup.find_all("h2", class_="section-title")

    # located rows
    shots_xg_rows = find_stat_rows("Shots, xG & Offsides", identifiers)
    goals_scored_rows = find_stat_rows("Goals Scored", identifiers)
    basic_stats_rows = find_stat_rows("Statistics", identifiers)

    # extracted stats in a list format

    # gsr for computing conversion rate ontarget
    gsr = find_stat("Scored / Match", goals_scored_rows, num=True)

    total_shots = find_stat("Shots / Match", shots_xg_rows, num=True)
    avg_shots_ontarget = find_stat("Shots On Target / Match", shots_xg_rows, num=True)
    avg_shots_offtarget = find_stat("Shots Off Target / Match", shots_xg_rows, num=True)
    conv_rate = find_stat("Shots Conversion Rate", shots_xg_rows, num=True)
    conv_rate_ontarget = calc_conv_rate_ontarget(gsr, avg_shots_ontarget)
    shots_per_goal = find_stat("Shots Per Goal Scored", shots_xg_rows, num=True)
    shots_ontarget_per_goal = find_stat(
        "Shots On Target Per Goal Scored", shots_xg_rows, num=True
    )
    xg_for = find_stat("XG FOr", shots_xg_rows, num=True)
    xg_against = find_stat("XG Against", shots_xg_rows, num=True)
    avg_poss = find_stat("Possession AVG", basic_stats_rows, num=True)

    return clean_stats(
        {
            "total_shots": total_shots,
            "avg_shots_ontarget": avg_shots_ontarget,
            "avg_shots_offtarget": avg_shots_offtarget,
            "conv_rate": conv_rate,
            "conv_rate_ontarget": conv_rate_ontarget,
            "shots_per_goal": shots_per_goal,
            "shots_ontarget_per_goal": shots_ontarget_per_goal,
            "xg_for": xg_for,
            "xg_against": xg_against,
            "avg_poss": avg_poss,
        },
        team_id,
    )


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

            parsed_team_stats = parse_team_stats(page_source, team_id)
            TEAMS_STATS.append(parsed_team_stats)

        except Exception as err:
            print(f"Oops! could not scrape the url '{team_url}'.")
            print(err)
            continue

    return TEAMS_STATS


""" Todo: Scraped Teams:
        - England teams ---done!
        - Germany ---done!
        - Spain --done!
        - France and Italy ---done!
        - Netherlands and Portugal ---done!
        - Austria, Denmark ---done!
        - Sweden and Norway --Finished
        - Czech and Switzerland ---done!
        - Belgium and Scotland ---done!
        - Israel, greece, turkey ---done!
"""
