""" 
    todo: Parameters to scrape. They are arranged based on their priority
        # refresh time for primatips is approx. 1 hour
        # refresh time for footystats is approx. 
        @primatips
            - Matches played               
            - Goals scored
            - Goals conceded
            - Gsr
            - Gcr
            - Clean sheets
            - Fts
        @footystats
            - Shots per game
            - Shots on target per game
            - Shots off target per game
            - XG for
            - XG against
            - Possesion per game

        @sofascore or flashscore or somewhere
            - Big chances
            - Attacks
            - Dangerous attacks
            
            - Computables => 
                - conversion rate
                - conversion rate ontarget
                - Shots per goal scored
                - Shots ontarget per goal scored

    todo: League stats parameters
        @footystats
            - League name
            - Country
            - Division
            - Number of teams
        @primatips
            - Number of Matches in the league
            - Number of matches played
            - Number of matches remaining
            - League progress(%)
            - Season  ###from here upward for now###
            - Avg goals
            - Gsr home
            - Gsr away
            - Gsf home
            - Gsf away
            - Win% home
            - Win% away
            - Draw%
            - Totals and btts (%)

"""

"""
    todo: scrape relevant stats and info for the selected league at "primatips.com"
        - Name
        - Country
        - Leauge Progress (%)
        - Matches Played
        - Remaining Matches
        - Avg Goals
        - Gsr Home
        - Gsr Away

    todo: scrape primatips parameters for all the teams in the selected league
        - Matches played
        - Goals scored
        - Goals conceded
        - GSR home/away
        - GCR home/away
        - FTS home/away
        - Clean sheets home/away

    todo: save the data into into supabase
        - Create necessary tables
        - Make the necessary foreing keys
        - Save the data appropriately        

"""
