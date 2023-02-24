**Throwers and Receivers Dashboard**

- Player: throw selection, teammate, both (by ~~game~~, season)
    * select team and player
    * show completion percentage
    * show throw selection and throwing teamate (and both)
    * show throwing distribution
- Team top Throws (thrower, receivers), (dump, dish, huck, break)
    * select team and throw; select thrower or receivers (or show both side to side)
    * show completion percentage
    * show top thrower and receivers
    * show throws distribution
- Comparing Teams
    * select throw / plays 
    * show team with highest throw attempt / completion
    * Comparing Team tendencies
- Comparing Players
    * which players are the most alike? similar roles
    * players roles evolution across the year 
    * compare young player with older player to imitate skillset
    * Dimension reduction: t-sne
	+ on throwing tendencies
	+ on scoring performance
    * 
- Team Victories
    * select division
    * plot directed graph for team victory: the more you win against 
      team, the more edge is heavier (change color:green to red)
- Team top def
- Team: game play, 
- Lineup Builder
    * duos/trios/quatuor with most off conversion / def conversion
- Player Chemistry
    * weighted graph
    * list of duos/trios/quatuors

**Team Victory Prediction Dashboard**




**Databases (deprecated)**

- Events
    * game_id
    * point_id
    * thrower_id
    * receiver_id
    * throwing_type_id
    * time_stamp
    * season_year
- Player
    * player_id
    * first_name
    * last_name
    * birth_date
    * season_year
    * team
- Team
    * team_id

**Fetching the Data**

- Game Events for game in season 2020, 2021, 2022
- Fetch Player
- Fetch Team


## TODOs

- [X] why event['r'] doesnt exists with t==3 sometimes (skipped if error)
- [X] compute for several games
- [X] fix when selecting all games: key error with 'game'
- [X] Pull distance is too big
- [X] make sure that team throwing dataset has only data from team 
- [X] Remove 'Pull' from 'Team Throwing Selection'
- [X] add receiver_id in 'Top Receivers'
- [X] refractor utils into:

**Player Throwing Selection**

- [ ] Add foreside or breakside in Player Throwing selection
- [ ] add plots

**Team Chemistry**

- [X] Get Lineup outcomes by points as json (audl API)
- [X] Compute Players Efficiency
- [ ] compute for all games

**Cluster**

- [X] doesn't show all players for royal on clustering
- [X] Add sliders for hyperparameters

## Ressources


- [Streamlit Database Connection](https://docs.streamlit.io/knowledge-base/tutorials/databases)
- [How to use graph theory to scout soccer](https://www.kdnuggets.com/2022/11/graph-theory-scout-soccer.html)
- [Network Analysis with Python](https://www.youtube.com/watch?v=x6PNcuZk83g)


