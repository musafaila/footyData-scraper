from fuzzywuzzy import fuzz


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
            name_score = fuzz.ratio(teamA["name"], teamB["primatips_name"])

            # Consider exact URL match as a strong indicator (if available)
            url_score = (
                100 if teamA["name"].lower() in teamB["primatips_url"].lower() else 0
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


def add_teams_urls(teams_data, leagues_db_data, **kwargs):

    try:
        scraping_func = kwargs.get("scraping_func")
        req = kwargs.get("req")
        driver = kwargs.get("driver")
        league_index = kwargs.get("league_index")
        save_to_json = kwargs.get("save_to_json")

        # select leagues based on the given index
        selected_league = leagues_db_data[league_index]
        # Filter teams based on league_id
        selected_teams = [
            team for team in teams_data if team["league_id"] == selected_league["id"]
        ]

        # NOTE: league_data is expected to be a list, so you have to pass it as a list even if it is a single element.
        teams_info = scraping_func(req, **{"league_data": [selected_league]})

        data_to_merge = {"dataA": selected_teams, "dataB": teams_info}

        merged_data = merge_teams_with_similar_name(
            data_to_merge["dataA"], data_to_merge["dataB"]
        )

        league_name = selected_league.get("name")
        path = f"data/primatips/url_added/{league_name}.json"
        save_to_json(path, merged_data)

        print("Operation Successfull!")

        return "success"

    except Exception as err:
        print(f"Error while adding scraping URLS: {err}")
        return
