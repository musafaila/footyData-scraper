from fuzzywuzzy import fuzz

from lib.utils import save_to_json


"""
todo: Grab the league data json
todo: Grab the teams data json

todo: Loop through the league data json file and scrape the table url for the teams info of the indexed league. ==> dataB

todo: Filter through the teams data json for the teams whose league_id == indexed_league_id. ==> dataA

todo: give these data points to our merge_teams_with_similar_name function and it will return a list of mearged teams data from dataA and dataB (which are similar)

todo: save the merged data into json with the league name as the name path=data/primatips/url_added/{league_name}.json
"""


def merge_teams_with_similar_name(dataA, dataB):
    """
    Merges dataA and dataB dictionaries based on team names and other factors.

    Args:
        dataA: List of dictionaries containing team information with "name" key.
        dataB: List of dictionaries containing team information with "primatips_name" key.

    Returns:
        A list of dictionaries with merged data from dataA and dataB.
    """
    merged_data = []
    for teamA in dataA:
        # Find the best match in dataB based on a combination of factors
        best_match = None
        max_score = 0
        for teamB in dataB:
            # Calculate fuzzy string similarity score (Levenshtein distance)
            name_score = fuzz.ratio(teamA["name"], teamB["flashscore_name"])

            # Consider exact URL match as a strong indicator (if available)
            url_score = (
                100 if teamA["name"].lower() in teamB["flashscore_url"].lower() else 0
            )

            # Optionally, consider league information for additional validation

            # Combine scores for a weighted evaluation
            total_score = name_score * 0.8 + url_score * 0.2  # Adjust weights as needed

            if total_score > max_score:
                max_score = total_score
                best_match = teamB

        # print(
        #     {
        #         "team": teamA["name"],
        #         "best_match": best_match["primatips_name"],
        #         "score": max_score,
        #     }
        # )

        # Merge data with the best match found.
        merged_data.append({**teamA, **best_match})

    return merged_data


def add_teams_urls(filtered_teams, filtered_scraped_teams, league):

    try:

        data_to_merge = {"dataA": filtered_teams, "dataB": filtered_scraped_teams}

        merged_data = merge_teams_with_similar_name(
            data_to_merge["dataA"], data_to_merge["dataB"]
        )

        league_name = league.get("name")
        path = f"data/flashscore/url_added/{league_name}.json"

        print("Operation Successfull!")

        return {"data": merged_data, "path": path}

    except Exception as err:
        print(f"Error while adding scraping URLS: {err}")
        return


def add_site_urls(scraped_teams_data, teams_db_data, leagues_db_data):
    # scraped_teams_data: This is the data that is scraped from the site i.e the data to be mergerd
    # teams_db_data: This is the data of teams in our db, we merge the scraped data into this one
    # leagues_db_data: This is the data of leagues in our db, we use it to find best matches

    for league in leagues_db_data:
        # league_index = leagues_db_data.index(league)
        # filtered_league = league

        try:
            # Filter teams based on league_id
            filtered_teams = [
                team for team in teams_db_data if team["league_id"] == league["id"]
            ]
            filtered_scraped_teams = [
                team for team in scraped_teams_data if team["league_id"] == league["id"]
            ]

            merged_data = add_teams_urls(filtered_teams, filtered_scraped_teams, league)

            data = merged_data["data"]
            path = merged_data["path"]

            save_to_json(path, data)
        except Exception as error:
            print(error, league.get("name"))
            continue
