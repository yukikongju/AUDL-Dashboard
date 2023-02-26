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

- [ ] Add foreside or breakside in Player Throwing selection
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
- [ ] get player picture?

**Throwing Location Analysis**

- [ ] Is disc location Markovian?
- [ ] Discovering best strategy in each position using RL and probability (simulation)


## Paper: Understanding Throwing Selection in Ultimate using Social Network Analysis

Ideas:
- Previous work in other sports: NBA, NFL, 
- The problem: 
- What we learned:
    * understanding player chemistry
    * define roles in audl: make cluster from throwing distribution
    * understanding throw selection relative to field position
    * throwing sequences: (dump-swing), (huck-dish), ()

## Ressources


- [Streamlit Database Connection](https://docs.streamlit.io/knowledge-base/tutorials/databases)
- [How to use graph theory to scout soccer](https://www.kdnuggets.com/2022/11/graph-theory-scout-soccer.html)
- [Network Analysis with Python](https://www.youtube.com/watch?v=x6PNcuZk83g)
- [Streamlit agraph](https://github.com/ChrisDelClea/streamlit-agraph)
- [Stanford CS224W - Analysis of Network Projects](http://snap.stanford.edu/class/cs224w-2017/projects.html)
- [Custom url in streamlit](https://discuss.streamlit.io/t/custom-domain-for-streamlit-sharing/8751/5)


