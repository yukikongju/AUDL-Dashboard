Field Size: 
53.5 yards wide; 80 yard long + 20 yards long
df: y_field == length (0,120); x_field == (-28, 28)

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
    * graph connections: 
	+ nodes_between: form group (see rivzikmath)
	+ strongly connected component (see The Historical Network Research Community)
- Player Chemistry
    * weighted graph
    * list of duos/trios/quatuors

**Team Victory Prediction Dashboard**


**Fetching the Data**

- Game Events for game in season 2020, 2021, 2022
- Fetch Player
- Fetch Team


## TODOs

1. Team Throwing: Throwing Sequence
2. Team Chemistry: Graph
3. RL Simulation: EV for disc location


- [X] why event['r'] doesnt exists with t==3 sometimes (skipped if error)
- [X] compute for several games
- [X] fix when selecting all games: key error with 'game'
- [X] Pull distance is too big
- [X] make sure that team throwing dataset has only data from team 
- [X] Remove 'Pull' from 'Team Throwing Selection'
- [X] add receiver_id in 'Top Receivers'
- [X] refractor utils into:

**Player Throwing Selection**

- [ ] TODO: Add foreside or breakside in Player Throwing selection
- [ ] TODO: Throw Heatmap -> probability of completion on the field for each throw
- [ ] add plots


**Team Throwing Selection**

- [ ] Add Download Button for dataset
- [X] Add Throwing Sequences + side: pairings (2,3,4)

**Team Chemistry**

- [X] Get Lineup outcomes by points as json (audl API)
- [X] Compute Players Efficiency
- [X] compute for all games
- [X] FIX: percentage pretty print
- [ ] FIX: don't call API when changing pairings
- [ ] FIX: off and defensive count are not accurate

**Cluster**

- [X] doesn't show all players for royal on clustering
- [X] Add sliders for hyperparameters

**Graph**

- [ ] Make weighted graph for throws
- [ ] TODO: add in/out degrees: 'throwed', 'received'
- [ ] get player picture?
- [ ] add player audl page when clicking on node
- [ ] Social Network Analysis Components: is the team system or individual based
    - [ ] In and out degrees
    - [ ] Betweeness:
    - [ ] Reciprocity:
    - [ ] Density:
    - [ ] Link Analysis
    - [ ] Community Detection

**Throwing Location Analysis**

- [ ] Is disc location Markovian?
- [ ] Discovering best strategy in each position using RL and probability (simulation)


## Paper: Understanding Throwing Selection in Ultimate using Social Network Analysis

- Why? determine if team strategy is player/team based and compare teams
Ideas:
- Previous work in other sports: NBA, NFL, 
- The problem: 
- What we learned:
    * understanding player chemistry
    * define roles in audl: make cluster from throwing distribution
    * understanding throw selection relative to field position
    * throwing sequences: (dump-swing), (huck-dish), ()


## Paper: Understanding best throwing decisions and disc location based on RL

- Condition on team and season
- Hypotheses: 
    * Player Agnostic: doesn't take player abilities into account
    * Position agnostic: doesn't take if player is cutter/thrower (throwing) 
      (throwing abilities won't be the same)
- How to simulate best decision using RL:
    * Environment state: continuous/discrete
    * Probability transition: weighted sum of success rate of throw inside range? + bayesian conditioning? (turnover or not, )
    * 

- Visualize throwing decision on the field

## Paper: Understanding player fatigue across the game/season using time series analysis

- Why? Load management
- Performance Prediction: how will the player perform given they play n points next game
- Conditioning
- Decomposition, seasonality
- Additional Questions: 
    * if a player plays less, will it improve next games performance?

- [ ] Fetch all throws for all games and save them in files
- [ ] Compute throw success based on team (conditionned by: team, (x, y), throwing type)
- [ ] Build RL environment
	* Actions state: [types of throws] pass, dish, dump, huck
	* Environment State: [throwing outcome] success, throwaway
	* Reward: pass (+1), goal (+100), throwaway (-50)



## Troubleshooting

**Pyviz doens't work**


## Ressources


- [Streamlit Database Connection](https://docs.streamlit.io/knowledge-base/tutorials/databases)
- [How to use graph theory to scout soccer](https://www.kdnuggets.com/2022/11/graph-theory-scout-soccer.html)
- [Network Analysis with Python](https://www.youtube.com/watch?v=x6PNcuZk83g)
- [Streamlit agraph](https://github.com/ChrisDelClea/streamlit-agraph)
- [Stanford CS224W - Analysis of Network Projects](http://snap.stanford.edu/class/cs224w-2017/projects.html)
- [Custom url in streamlit](https://discuss.streamlit.io/t/custom-domain-for-streamlit-sharing/8751/5)
- [streamlit agraph stroke width](https://discuss.streamlit.io/t/showing-off-the-streamlit-agraph-component/6712/8)
- [pyvis interactive networks](https://discuss.streamlit.io/t/interactive-networks-graphs-with-pyvis/8344)
- [sibling package imports using setup.py](https://stackoverflow.com/questions/6323860/sibling-package-imports/50193944#50193944)


