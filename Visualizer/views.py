import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
import pandas as pd
import streamlit as st
import textwrap

## this file contains code for different visualzation/ views of the LePa visualizer --> aka model

options = {
   "nodes": {
     "borderWidth": 3,
     "borderWidthSelected": 6,
     "shadow": {
       "enabled": True,
       "color": "white",
       "size": 9,
       "x": -1,
       "y": -2
     },
     "shapeProperties": {
       "borderRadius": 4
     },
     "size": 29
   },
   "edges": {
     "color": {
       "inherit": True
     },
     "dashes": True,
     "font": {
       "strokeWidth": 5
     },
     "hoverWidth": 3.2,
     "scaling": {
       "label": {
         "min": 24
       }
     },
     "selfReference": {
       "angle": 0.7853981633974483
     },
     "smooth": {
       "roundness": 0.7
     }
   },
   "interaction": {
     "hideEdgesOnZoom": True,
     "hover": True,
     "keyboard": {
       "enabled": True
     },
     "multiselect": True,
     "navigationButtons": True
   },
   "manipulation": {
     "enabled": True
   },
   "physics": {
     "minVelocity": 0.75
   }
 }
 
#########################################################################
def viewAll(uploaded_file, physics):
  df = pd.read_csv(uploaded_file)
  # fill empty cells in specifc column with nil
  df["Alternative"].fillna("nil", inplace = True) 
  df_id = df['ID']
  df_title = df['Title']
  df_alt = df['Alternative']
  df_tURL = df['targetUrl']
  df_type = df['Type']
  df_isPartOf = df['isPartOf']
  df_assesses = df['assesses']
  df_requires = df['requires']

  data_ER = zip(df_id, df_title, df_alt, df_tURL, df_type, df_isPartOf, df_assesses, df_requires) # making tuples  
  G = nx.DiGraph()
  for d in data_ER:
    d_id = d[0]
    d_title = d[1]
    d_type = d[4]
    d_alt = d[2]
    if(d_type=="aER"):
      G.add_node(d_id, label = d_title, shape="box", title=d_alt)
    elif(d_type == "rER"):
      G.add_node(d_id, label = d_title, shape="triangle", title=d_alt) 
    elif(d_type == "iER"):
      G.add_node(d_id, label = d_title, shape="circle", title=d_alt)
    else:
      G.add_node(d_id, label = d_title, title=d_alt)
        
    ## relationship assesses:
    d_assesses = d[6]
    data_assess = zip(df_id)
    for d1 in data_assess:
      d1_id = d1[0]
      if(d_assesses == d1_id):
        G.add_edge(d_id, d1_id, color="red")
        
    ## relationship requires:
    d_requires = d[7]
    data_req = zip(df_id)
    for d2 in data_req:
      d2_id = d2[0]
      if(d_requires == d2_id):
        #use label to label the edges
        G.add_edge( d2_id, d_id, weight = 5)

    ## relationship isPartOf:
    d_isPartOf = d[5]
    data_isPartOf = zip(df_id)
    for d3 in data_isPartOf:
      d3_id = d3[0]
      if(d_isPartOf == d3_id):     
        G.add_edge( d3_id,d_id, color = "green")

  G2 = Network(height="800px", width="100%", bgcolor="#222222", font_color="white", notebook=True,heading='', directed=True)
  G2.from_nx(G)
  if physics:
    G2.height = "500px"
    G2.show_buttons()
  else:
    G2.options = options
  for node in G2.nodes:
    id_string = node["label"]
    width = 10
    wrapped_strings = textwrap.wrap(id_string, width)
    wrapped_id =""; 
    for line in wrapped_strings:
      wrapped_id = textwrap.fill(id_string, width)
    node["label"] = wrapped_id
    
  G2.show('viewAll.html')

########################################################################    
def view_2(uploaded_file):
  # df = pd.read_csv(uploaded_file)
  # # fill empty cells in specifc column with nil
  # df["Alternative"].fillna("nil", inplace = True) 
  # df_id = df['ID']
  # df_title = df['Title']
  # df_alt = df['Alternative']
  # df_tURL = df['targetUrl']
  # df_type = df['Type']
  # df_isPartOf = df['isPartOf']
  # df_assesses = df['assesses']
  # df_requires = df['requires']
    
  # data_ER = zip(df_id, df_title, df_alt, df_tURL, df_type, df_isPartOf, df_assesses, df_requires) # making tuples  
  G = nx.DiGraph()
  # for d in data_ER:  
  #   d_id = d[0]
  #   d_title = d[1]
  #   d_type = d[4]
  #   d_alt = d[2]
  #   if(d_type=="aER"):
  #     G.add_node(d_id, label = d_title, shape="box", title=d_alt)
  #   elif(d_type == "rER"):
  #     G.add_node(d_id, label = d_title, shape="triangle", title=d_alt) 
        
  #   ## relationship assesses:
  #   d_assesses = d[6]
  #   data_assess = zip(df_id)
  #   for d1 in data_assess:
  #     d1_id = d1[0]
  #     if(d_assesses == d1_id):
  #       G.add_edge(d_id, d1_id, color="red")
  G.add_node("A")
  G.add_node("B")
  G.add_node("C")
  G.add_node("D")
  G.add_edge("A", "B")
  M = nx.identified_nodes(G, "A", "B", self_loops=False)
  G2 = Network(height="800px", width="100%", bgcolor="#222222", font_color="white", notebook=True,heading='', directed=True)
  G2.from_nx(M)
  G2.options = options
  for node in G2.nodes:
    id_string = node["label"]
    width = 10
    wrapped_strings = textwrap.wrap(id_string, width)
    wrapped_id =""; 
    for line in wrapped_strings:
      wrapped_id = textwrap.fill(id_string, width)
    node["label"] = wrapped_id
    
    G2.show('view2.html') 
