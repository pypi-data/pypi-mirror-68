# leaguepedia_parser
A parser for the Leaguepedia website, focused on accessing esports data.

Possible future functionality includes  direct querying for games from team names, fuzzy matching for tournament names, .... Any help is welcome, I am currently only adding features that I use on my projects.

# Install
`pip install leaguepedia_parser`

# Usage
```python
import leaguepedia_parser

lp = leaguepedia_parser.LeaguepediaParser()

# Gets you available regions
lp.get_tournament_regions()

# Gets you tournaments in the region, by default only returns primary tournaments
tournaments = lp.get_tournaments('Korea', year=2020)

# Gets you all games for a tournament. Get the name from get_tournaments()
games = lp.get_games(tournaments[0]['name'])

# Gets picks and bans for a game. Get the game object from get_games()
lp.get_picks_bans(games[0])

# Gets the URL of the team’s logo
lp.get_team_logo('T1')

# Get player’s info
lp.get_player('Faker')
```

More usage examples can be found in the `_tests` folder where every function is tested at least once.

# river_mwclient

If you installed `river_mwclient`, the `LeaguepediaParser` class will inherit from its `EsportsClient` class.

If not, it
will simply be a wrapper for `mwclient`.
