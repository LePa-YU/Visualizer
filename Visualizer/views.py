import networkx as nx
import pyvisToHtml
from pyvis.network import Network
import pandas as pd
import streamlit as st
import textwrap
import sys

## this file contains code for different visualzation/ views of the LePa visualizer --> aka model

def setData(df):
  # fill empty cells in specifc column with nil
  df.columns = df.columns.str.lower()
  
  global df_id
  try:
    df_id = df['id']
  except:
    df['id'] =""
    df_id = df['id']

  global df_title
  try:
    df_title = df['title']
  except:
    df['title'] = ""
    df_title = df['title']

  global df_alt
  try:
    df["alternative"].fillna("nil", inplace = True)
    df_alt = df['alternative']
  except:
    df['alternative']=""
    df_alt = df['alternative']

  global df_tURL
  try:
    df['targeturl'].fillna("nil", inplace = True)
    df_tURL = df['targeturl']
  except:
    df['targeturl'] =""
    df_tURL = df['targeturl']

  global df_type
  try:
    df_type = df['type']
  except:
    df['type'] = ""
    df_type = df['type']

  global df_isPartOf
  try:
    df_isPartOf = df['ispartof']
  except:
    df['ispartof'] = ""
    df_isPartOf = df['ispartof']

  try:
    df_assesses = df['assesses']
  except:
    df['assesses'] = ""
    df_assesses = df['assesses']
  
  try:
    df_requires = df['requires']
  except:
    df['requires']=""
    df_requires = df['requires']
  
  try:
    df_comesAfter = df['comesafter']
  except:
    df['comesafter']=""
    df_comesAfter = df['comesafter']

  try:
    df_comesAfter_aER = df["comesafter_aer"]
  except:
    df["comesafter_aer"]=""
    df_comesAfter_aER = df["comesafter_aer"]
  
  global data_ER
  data_ER = zip(df_id, df_title, df_alt, df_tURL, df_type, df_isPartOf, df_assesses, df_requires, df_comesAfter, df_comesAfter_aER) # making tuples 

# initial options
physics = {
     "minVelocity": 0.75
}
layout = {
    "randomSeed":10
  }
manipulation = {
     "enabled": True
}
interaction = {
     "hideEdgesOnZoom": True,
     "hover": True,
     "keyboard": {
       "enabled": True
     },
     "multiselect": True,
     "navigationButtons": True
   
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

# method  that converst networkx to pyvis
def convert_to_pyvis(G, file_name):
  G2 = Network(height="800px", width="100%", bgcolor="white", font_color=setFontColor("white"), notebook=True,heading='', directed=True)
  G2.from_nx(G)
  G2.options.edges = edges
  G2.options.nodes = nodes
  G2.options.interaction = interaction
  G2.options.manipulation = manipulation
  G2.options.layout = layout
  
  for node in G2.nodes:
    id_string = node["label"]
    width = 15
    wrapped_strings = textwrap.wrap(id_string, width)
    wrapped_id =""; 
    for line in wrapped_strings:
      wrapped_id = textwrap.fill(id_string, width)
    node["label"] = wrapped_id

  data = G2.get_network_data()
  pyvisToHtml.convertToHtml(data, file_name)

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
def All_ERs():
  # setColors()
  G = nx.DiGraph()
  for d in data_ER:
    d_id = d[0]
    d_title = d[1]
    d_type = d[4]
    d_alt = d[2]
    d_isPartOf = d[5]
    if(d_type=="aER"):
      G.add_node(d_id, label = d_title, shape="box", title=d_alt, color= aER_node_color)
    elif(d_type == "rER"):
      G.add_node(d_id, label = d_title, shape="triangle", title=d_alt, color = rER_node_color) 
    elif(d_type == "iER"):
      G.add_node(d_id, label = d_title, shape="circle", title=d_alt, color= iER_node_color)
    else:
      G.add_node(d_id, label = d_title, title=d_alt, color= general_node_color, isPartOf=int(d_isPartOf))
        
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

    ## relationship comesAfter:
    d_comesAfter = d[8]
    data_ca = zip(df_id)
    for d2 in data_ca:
      d2_id = d2[0]
      if(d_comesAfter == d2_id):
        #use label to label the edges
        G.add_edge( d2_id, d_id, weight = 5, color= requires_edge_color)

    ## relationship isPartOf:
    # d_isPartOf = d[5]
    data_isPartOf = zip(df_id)
    for d3 in data_isPartOf:
      d3_id = d3[0]
      if(d_isPartOf == d3_id):     
        G.add_edge( d3_id,d_id, color = isPartOf_edge_color)
  file_name = "All_ERs.html"
  convert_to_pyvis(G, file_name)

########################################################################    
def Course_Overview():
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
    
    ## relationship comesAfter:
    d_comesAfter = d[8]
    data_ca = zip(df_id)
    for d2 in data_ca:
      d2_id = d2[0]
      if(d_comesAfter == d2_id):
        #use label to label the edges
        G.add_edge( d2_id, d_id, weight = 5, color= requires_edge_color)
  
  file_name = "Course_Overview.html"
  convert_to_pyvis(G,file_name)

##########################################################
########################################################################    
def Summative_assessment_only():
  # setColors()
  G = nx.DiGraph()
  for d in data_ER:
    d_id = d[0]
    d_title = d[1]
    d_type = d[4]
    d_alt = d[2]
    d_isPartOf = d[5]
    if(d_type=="aER"):
      G.add_node(d_id, label = d_title, shape="box", title=d_alt, color= aER_node_color)
    elif(d_type == "rER"):
      G.add_node(d_id, label = d_title, shape="triangle", title=d_alt, color = rER_node_color) 
   
        
    ## relationship assesses:
    d_assesses = d[6]
    data_assess = zip(df_id)
    for d1 in data_assess:
      d1_id = d1[0]
      if(d_assesses == d1_id):
        G.add_edge(d_id, d1_id, color= assess_edge_color)

    ## relationship comesAfter:
    d_comesAfter_aER = d[9]
    data_ca = zip(df_id)
    for d2 in data_ca:
      d2_id = d2[0]
      if(d_comesAfter_aER == d2_id):
        #use label to label the edges
        G.add_edge( d2_id, d_id, weight = 5, color= requires_edge_color)
  
  file_name = "Summative_assessment_only.html"
  convert_to_pyvis(G,file_name)

########################################################################    
def create_Legend():
  # setColors()
  G = nx.DiGraph()
                    
  G.add_node(1, label = "Activity ER      ", shape = "text", title="legend", color= aER_node_color, x = 0, y = 0)
  G.add_node(2, label = "       ", shape="box", title="legend", color= aER_node_color, x = 100, y = 0)
  
  G.add_node(3, label = "Rubric ER        ", shape="text", title="legend", color = rER_node_color, x = 0, y = 50 )
  G.add_node(4, label = "", shape="triangle", title="legend", color = rER_node_color, x = 100, y = 50 ) 

  G.add_node(5, label = "Instructional ER ", shape="text", title="legend", color= iER_node_color, x = 0, y = 100)
  G.add_node(6, label = "    ", shape="circle", title="legend", color= iER_node_color, x = 100, y = 100)

  G.add_node(7, label = "Non-composite iER", title="legend", shape = "text", color= general_node_color, x = 0, y = 150)
  G.add_node(0, label = "", title="legend", color= general_node_color, x = 100, y = 150)

  G.add_node(8, label = "Assesses", title="legend", shape = "text", color= general_node_color, x = 200, y = 0)
  G.add_node(9, label = " ",title="legend", shape="text", x = 250, y = 0)
  G.add_node(10, label = " ",title="legend", shape="text", x = 400, y = 0)
  G.add_edge(9, 10,color= assess_edge_color)
  
  G.add_node(11, label = "Requires", title="legend", shape = "text", color= general_node_color, x = 200, y = 50)
  G.add_node(12, label = " ",title="legend", shape="text", x = 250, y = 50)
  G.add_node(13, label = " ",title="legend", shape="text", x = 400, y = 50)
  G.add_edge(12, 13,weight = 5, color= requires_edge_color)
 
  G.add_node(14, label = "isPartOf", title="legend", shape = "text", color= general_node_color, x = 200, y = 100)
  G.add_node(15, label = " ",title="legend", shape="text", x = 250, y = 100)
  G.add_node(16, label = " ",title="legend", shape="text", x = 400, y = 100)
  G.add_edge(15, 16, color = isPartOf_edge_color)

  G2 = Network(height="800px", width="100%", bgcolor="white", font_color=setFontColor("white"), notebook=True,heading='', directed=True)
  G2.from_nx(G)
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
    
     "fixed": {
      "x": True,
      "y": True
    }
}
  interaction = {
     "hover": True,
     "dragNodes": False,
    "dragView": False,
    "zoomView": False,
    "navigationButtons": True,

}
  G2.options.edges = edges
  G2.options.nodes = nodes
  G2.options.layout = layout
  G2.options.interaction = interaction
  data = G2.get_network_data()
  pyvisToHtml.convertToHtml_Legend(data)
  
  