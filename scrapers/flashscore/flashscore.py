

"""
todo: scrape all the fixtures and filter those whose time is tomorrow

todo: loop through each fixture and:
    todo: grab their round fixture = {fixture_round, fixture}
    todo: click each fixture to open in new window and grab it's link
    todo: add it to the previous object {fixture_round, fixture_url}
    todo: close the previous window
    todo: append to a list

todo: save the list into db

league_id
home_id
away_id
date
kickoff
url
round

"""


def flashscore_fixtures_scraper(driver):

   pass

   fixtures_container = "sportName soccer"
   fixtures_round = "event__round event__round--static"
   fixture = "event__match event__match--static event__match--scheduled event__match--twoLine"
   fixture_time = "event__time"