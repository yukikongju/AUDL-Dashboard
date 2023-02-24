import requests
import streamlit as st
import pandas as pd
import audl 

st.markdown("# Welcome to the AUDL Dashboard!")

st.write("This dashboard aims to gain insights on ...")

description = """
1. Teams and Players Throwing Selection
    * For players: what throws are each likely to throw? what is their throwing percentage for the given throw? who are they throwing to?
    * For teams: which players are hucking? dumping? swinging? who are they throwing to?
2. Team Chemistry and Lineup Builder
    * which duos/trios/quatuors are the most successful together / have the most chemistry? we want to assess point conversion rate
3. Comparing Players and Teams Performance
    * which teams/player distinguishes themselves? how do they differ in terms of (1) their stats/throwing selection?
    * we will be performing dimension reduction and clustering
4. Players Fatigue
    * how efficient is a player as the game progress? we track the number of touches, turnovers, ...
"""
st.write(description)



st.write('### Ressources')

ressources = """
All data where pulled from the [official audl website](https://theaudl.com)
using the [unofficial AUDL API](https://github.com/yukikongju/audl)
"""
st.write(ressources)

st.write('### Suggestions')

suggestions = """
For any suggestions, please contact yukikongju@outlook.com
""" 
st.write(suggestions)
