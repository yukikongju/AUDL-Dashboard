import streamlit as st
import networkx as nx
import pandas as pd
import math
from streamlit_agraph import agraph, Node, Edge, Config

def generate_connections_graph(df_throws, throw_type, thrower_receiver_radiobox):
    # 0. remove pull and throwaway
    if throw_type != 'All':
        df_throws = df_throws[df_throws['throw_type'] == throw_type]

    # 1. count throws by throw type
    df_count = df_throws.groupby(['receiver_full_name', 'thrower_full_name'])['throw_type'].count().reset_index(name = 'count')

    node_column = 'thrower_full_name' if thrower_receiver_radiobox == 'Thrower' else 'receiver_full_name'

    # compute node size based on player total count
    df_players = df_count.groupby([node_column])['count'].sum().reset_index()
    max_val = max(df_count['count'])
    df_players['node_size'] = df_players['count'].apply(lambda x: math.log(1+ x/max_val) * 20)


    # init nodes and edges
    nodes = []
    
    for _, row in df_players.iterrows():
        nodes.append(Node(id=row[node_column], label=row[node_column], size=row['node_size']))


    # TODO: compute edge color based on thrower/receiver connection
    min_val = min(df_count['count'])
    max_val = max(df_count['count'])

    edges = []
    for _, row in df_count.iterrows():
        #  hex_color = compute_edge_color(row['count'], min_val, max_val)
        edges.append(Edge(source=row['thrower_full_name'], target=row['receiver_full_name'], label=row['count'], color='#008B8B'))

    #  st.write(df_players)
    #  st.write(df_count)

    config = Config(width=850,
                height=850,
                directed=True, 
                physics=True, 
                hierarchical=False,
                collapsible=False
            )

    graph = agraph(nodes, edges, config) 


def compute_edge_color(value, min_val, max_val):
    b = (value - min_val) // (max_val - min_val) * 255
    return rgb_to_hex(150, 150, b)

def rgb_to_hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)

    
    
