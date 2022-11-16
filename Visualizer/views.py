import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
import pandas as pd
import streamlit as st
import textwrap

## this file contains code for different visualzation/ views of the LePa visualizer --> aka model

def setData(df):
  # df = pd.read_csv(uploaded_file)
  # fill empty cells in specifc column with nil
  df.columns = df.columns.str.lower()
  df["alternative"].fillna("nil", inplace = True) 
  global df_id
  df_id = df['id']
  global df_title
  df_title = df['title']
  global df_alt
  df_alt = df['alternative']
  df_tURL = df['targeturl']
  global df_type
  df_type = df['type']
  global df_isPartOf
  df_isPartOf = df['ispartof']
  df_assesses = df['assesses']
  df_requires = df['requires']
  global data_ER
  data_ER = zip(df_id, df_title, df_alt, df_tURL, df_type, df_isPartOf, df_assesses, df_requires) # making tuples 


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
     "size": 29,
      
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
   "layout": {
    "randomSeed":10
  },
   "physics": {
     "minVelocity": 0.75
   }
 }
edges = {
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
 }
nodes = {
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
     "size": 29,
}
def convert_to_pyvis(G,bg, physics, fix):
  G2 = Network(height="800px", width="100%", bgcolor=bg, font_color=setFontColor(bg), notebook=True,heading='', directed=True)
  G2.from_nx(G)
  G2.options.edges = edges
  G2.options.nodes = nodes
  if physics and not fix:
    G2.height = "500px"
    G2.show_buttons()
  else:
    # G2.options = options
    if fix:
      n = nodes
      n.update({ "fixed": {
      "x": True,
      "y": True
    }})
      G2.options.nodes = n
      G2.toggle_drag_nodes(False)
    else:
      G2.toggle_drag_nodes(True)
      n = nodes
      n.update({ "fixed": {
      "x": False,
      "y": False
    }})

  for node in G2.nodes:
    id_string = node["label"]
    width = 10
    wrapped_strings = textwrap.wrap(id_string, width)
    wrapped_id =""; 
    for line in wrapped_strings:
      wrapped_id = textwrap.fill(id_string, width)
    node["label"] = wrapped_id
    
    
    
  G2.show('view.html')
#########################################################################

def setColors(aER, rER, iER, general, assess, requires, isPartOf):
  global aER_node_color
  aER_node_color = aER
  global rER_node_color
  rER_node_color = rER
  global iER_node_color
  iER_node_color = iER
  global general_node_color
  general_node_color = general
  global assess_edge_color
  assess_edge_color = assess
  global requires_edge_color
  requires_edge_color = requires
  global isPartOf_edge_color
  isPartOf_edge_color = isPartOf

def setFontColor(bg):
  # set font color based on bg:
  font_color = ""
  if(bg=="white"):
    font_color = "black"
  else:
    font_color = "white"
  return font_color
 
#########################################################################
def viewAll(physics, bg, fix):
  # setColors()
  G = nx.DiGraph()
  # data_ER = setData(uploaded_file)
  # df_id = get_Id_Rows(uploaded_file)
  for d in data_ER:
    d_id = d[0]
    d_title = d[1]
    d_type = d[4]
    d_alt = d[2]
    if(d_type=="aER"):
      G.add_node(d_id, label = d_title, shape="box", title=d_alt, color= aER_node_color)
    elif(d_type == "rER"):
      G.add_node(d_id, label = d_title, shape="triangle", title=d_alt, color = rER_node_color) 
    elif(d_type == "iER"):
      G.add_node(d_id, label = d_title, shape="circle", title=d_alt, color= iER_node_color)
    else:
      G.add_node(d_id, label = d_title, title=d_alt, color= general_node_color)
        
    ## relationship assesses:
    d_assesses = d[6]
    data_assess = zip(df_id)
    for d1 in data_assess:
      d1_id = d1[0]
      if(d_assesses == d1_id):
        G.add_edge(d_id, d1_id, color= assess_edge_color)
        
    ## relationship requires:
    d_requires = d[7]
    data_req = zip(df_id)
    for d2 in data_req:
      d2_id = d2[0]
      if(d_requires == d2_id):
        #use label to label the edges
        G.add_edge( d2_id, d_id, weight = 5, color= requires_edge_color)

    ## relationship isPartOf:
    d_isPartOf = d[5]
    data_isPartOf = zip(df_id)
    for d3 in data_isPartOf:
      d3_id = d3[0]
      if(d_isPartOf == d3_id):     
        G.add_edge( d3_id,d_id, color = isPartOf_edge_color)
  convert_to_pyvis(G,bg, physics, fix)

########################################################################    
def AIR_view(physics, bg, fix):
  # setColors()
  # data_ER = setData(uploaded_file)
  # df_id = get_Id_Rows(uploaded_file)
  G = nx.DiGraph()
  for d in data_ER:  
    d_id = d[0]
    d_title = d[1]
    d_type = d[4]
    d_alt = d[2]
    if(d_type=="aER"):
      G.add_node(d_id, label = d_title, shape="box", title=d_alt, color = aER_node_color)
    elif(d_type == "rER"):
      G.add_node(d_id, label = d_title, shape="triangle", title=d_alt, color = rER_node_color) 
    elif(d_type == "iER"):
      G.add_node(d_id, label = d_title, shape="circle", title=d_alt, color= iER_node_color)
        
    ## relationship assesses:
    d_assesses = d[6]
    data_assess = zip(df_id)
    for d1 in data_assess:
      d1_id = d1[0]
      if(d_assesses == d1_id):
        G.add_edge(d_id, d1_id, color= assess_edge_color)
    ## relationship requires:
    d_requires = d[7]
    data_req = zip(df_id)
    for d2 in data_req:
      d2_id = d2[0]
      if(d_requires == d2_id):
        G.add_edge( d2_id, d_id, weight = 5, color= requires_edge_color)

  convert_to_pyvis(G,bg, physics, fix)

##########################################################
########################################################################    
def view_3(physics, bg):
  G = nx.DiGraph()
  G.add_node("A", x=0, y=0)
  G.add_node("B", x=5, y = 0)
  G.add_node("C", x=10, y=0)
  G.add_node("D")
  G.add_edge("A", "B")
  G.add_edge("B", "C")
  G.add_edge("B", "D")
  pos = nx.spring_layout(G)
  # M = nx.identified_nodes(G, "A", "B", self_loops=False)
  
  # convert_to_pyvis(G,bg, physics)
  G2 = Network(height="800px", width="100%", bgcolor=bg, font_color=setFontColor(bg), notebook=True,heading='', directed=True)
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
    
  G2.show('view.html')
