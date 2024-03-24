 
"""
 def add_flash_urls(league_data: []):

    URLS = [
        "https://www.flashscore.com/football/switzerland/challenge-league/fixtures/",
        "https://www.flashscore.com/football/israel/ligat-ha-al/fixtures/",
        "https://www.flashscore.com/football/england/championship/fixtures/",
        "https://www.flashscore.com/football/germany/bundesliga/fixtures/",
        "https://www.flashscore.com/football/germany/2-bundesliga/fixtures/",
        "https://www.flashscore.com/football/germany/3-liga/fixtures/",
        "https://www.flashscore.com/football/spain/laliga/fixtures/",
        "https://www.flashscore.com/football/spain/laliga2/fixtures/",
        "https://www.flashscore.com/football/italy/serie-a/fixtures/",
        "https://www.flashscore.com/football/italy/serie-b/fixtures/",
        "https://www.flashscore.com/football/france/ligue-1/fixtures/",
        "https://www.flashscore.com/football/france/ligue-2/fixtures/",
        "https://www.flashscore.com/football/netherlands/eredivisie/fixtures/",
        "https://www.flashscore.com/football/netherlands/eerste-divisie/fixtures/",
        "https://www.flashscore.com/football/portugal/liga-portugal/fixtures/",
        "https://www.flashscore.com/football/portugal/liga-portugal-2/fixtures/",
        "https://www.flashscore.com/football/austria/bundesliga/fixtures/",
        "https://www.flashscore.com/football/austria/2-liga/fixtures/",
        "https://www.flashscore.com/football/denmark/superliga/fixtures/",
        "https://www.flashscore.com/football/denmark/1st-division/fixtures/",
        "https://www.flashscore.com/football/sweden/allsvenskan/fixtures/",
        "https://www.flashscore.com/football/sweden/superettan/fixtures/",
        "https://www.flashscore.com/football/norway/eliteserien/fixtures/",
        "https://www.flashscore.com/football/czech-republic/fortuna-liga/fixtures/",
        "https://www.flashscore.com/football/czech-republic/fnl/fixtures/",
        "https://www.flashscore.com/football/switzerland/super-league/fixtures/",
        "https://www.flashscore.com/football/belgium/jupiler-pro-league/fixtures/",
        "https://www.flashscore.com/football/belgium/challenger-pro-league/fixtures/",
        "https://www.flashscore.com/football/scotland/premiership/fixtures/",
        "https://www.flashscore.com/football/scotland/championship/fixtures/",
        "https://www.flashscore.com/football/cyprus/cyta-championship/fixtures/",
        "https://www.flashscore.com/football/greece/super-league/fixtures/",
        "https://www.flashscore.com/football/turkey/super-lig/fixtures/",
        "https://www.flashscore.com/football/england/premier-league/fixtures/",
        "https://www.flashscore.com/football/england/league-one/fixtures/",
        "https://www.flashscore.com/football/england/league-two/fixtures/",
        "https://www.flashscore.com/football/norway/obos-ligaen/fixtures/",
    ]

    UPDATED_DATA = []

    for i, data in enumerate(league_data):

        table_url = URLS[i].replace('fixtures', 'standings')

        data['flashscore_fixture_url'] = URLS[i]
        data['flashscore_table_url'] = table_url

        UPDATED_DATA.append(data)

        
    return UPDATED_DATA
 """


def add_league_table_url():
    pass
    # todo: Query the DB for leagues info
    # 