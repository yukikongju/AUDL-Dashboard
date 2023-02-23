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
- Comparing Players
    * which players are the most alike? similar roles
    * players roles evolution across the year 
    * compare young player with older player to imitate skillset
- Team Victories
    * select division
    * plot directed graph for team victory: the more you win against 
      team, the more edge is heavier (change color:green to red)
- Network graph
- Team top def
- Team: game play, 

**Team Victory Prediction Dashboard**




**Databases**

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

**Player Throwing**

- [X] why event['r'] doesnt exists with t==3 sometimes (skipped if error)
- [X] compute for several games
- [X] fix when selecting all games: key error with 'game'
- [X] Pull distance is too big
- [ ] add receiver_id in 'Top Receivers'
- [ ] add plots


## Ressources


- [Streamlit Database Connection](https://docs.streamlit.io/knowledge-base/tutorials/databases)


