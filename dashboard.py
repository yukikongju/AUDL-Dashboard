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
2. Lineup Builder
    * which duos/trios/quatuors are the most successful together? we want to assess point conversion rate
    * 
3. Players Fatigue
    * how efficient is a player as the game progress? we track the number of touches, turnovers, ...
    * 
"""
st.write(description)

#  st.write("##### What information can I find in this dashboard?")

suggestions = """

""" 
