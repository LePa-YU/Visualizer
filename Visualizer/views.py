import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
import pandas as pd
import streamlit as st
import textwrap
import json
import sys

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
def convert_to_pyvis(G,bg, physics, fix):
  G2 = Network(height="800px", width="100%", bgcolor=bg, font_color=setFontColor(bg), notebook=True,heading='', directed=True)
  G2.from_nx(G)
  G2.options.edges = edges
  G2.options.nodes = nodes
  G2.options.interaction = interaction
  G2.options.manipulation = manipulation
  G2.options.layout = layout

  if physics and not fix:
    G2.height = "500px"
    G2.show_buttons()
  if fix:
      n = nodes
      n.update({ "fixed": {
      "x": True,
      "y": True
      }})
      G2.options.nodes = n
      i = interaction
      i.update({"dragNodes": False})
      G2.options.interaction = i
      # G2.toggle_drag_nodes(False)
  else:
      # G2.toggle_drag_nodes(True)
      n = nodes
      n.update({ "fixed": {
      "x": False,
      "y": False
      }})
      i = interaction
      i.update({"dragNodes": True})
      G2.options.interaction = i
  x = 0
  for node in G2.nodes:
    id_string = node["label"]
    width = 10
    wrapped_strings = textwrap.wrap(id_string, width)
    wrapped_id =""; 
    for line in wrapped_strings:
      wrapped_id = textwrap.fill(id_string, width)
    node["label"] = wrapped_id
    # n = node.update({"x": x})
    
  #Extract info
  f = open('network.js', 'w')

  data = G2.get_network_data()
  nodes_data = data[0]
  jsonOb_node = json.dumps(nodes_data)
  jsonOb_node_format = format(jsonOb_node)
  f.write("var nodes = "+str(jsonOb_node_format) +";"+"\n")
  
  edges_data = data[1]
  jsonOb_edges = json.dumps(edges_data)
  jsonOb_edges_format = format(jsonOb_edges)
  f.write("var edges = "+str(jsonOb_edges_format) +";"+"\n")
  
  heading_data = data[2]
  jsonOb_heading = json.dumps(heading_data)
  jsonOb_heading_format = format(jsonOb_heading)
  f.write("var heading = "+str(jsonOb_heading_format) +";"+"\n")

  height_data = data[3]
  jsonOb_height = json.dumps(height_data)
  jsonOb_height_format = format(jsonOb_height)
  f.write("var height = "+str(jsonOb_height_format) +";"+"\n")

  width_data = data[4]
  jsonOb_width = json.dumps(width_data)
  jsonOb_width_format = format(jsonOb_width)
  f.write("var width = "+str(jsonOb_width_format) +";"+"\n")

  options_data = data[5]
  jsonOb_options = json.dumps(options_data)
  jsonOb_options_format = format(jsonOb_options)
  f.write("var options = "+str(jsonOb_options_format) +";"+"\n")   
    
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
def view_3(physics, bg, fix):
  G = nx.DiGraph()
  G.add_node(1, label="A", x=0, y=0)
  G.add_node(2, label="B", x=5, y = 0)
  G.add_node(3, label="C",x=10, y=0)
  # G.add_node("D")
  G.add_edge(1, 2)
  G.add_edge(2, 3)
  # G.add_edge("B", "D")
  # p={
  #   "A":[0, 10], 
  #   "B": [20, 10],
  #   "C": [30, 10]
  # }
  # M = nx.identified_nodes(G, "A", "B", self_loops=False)
  
  # convert_to_pyvis(G,bg, physics)
  G2 = Network(height="800px", width="100%", bgcolor=bg, font_color=setFontColor(bg), notebook=True,heading='', directed=True)
  G2.from_nx(G)
  if physics:
    G2.height = "500px"
    G2.show_buttons()
  # else:
    # G2.options = options
  # for node in G2.nodes:
  #   id_string = node["label"]
  #   width = 10
  #   wrapped_strings = textwrap.wrap(id_string, width)
  #   wrapped_id =""; 
  #   for line in wrapped_strings:
  #     wrapped_id = textwrap.fill(id_string, width)
  #   node["label"] = wrapped_id
  
  G2.options.edges = edges
  G2.options.nodes = nodes
  G2.options.interaction = interaction
  G2.options.manipulation = manipulation
  G2.options.layout = layout
  
  #Extract info
  f = open('network.js', 'w')

  data = G2.get_network_data()
  nodes_data = data[0]
  jsonOb_node = json.dumps(nodes_data)
  jsonOb_node_format = format(jsonOb_node)
  f.write("var nodes = "+str(jsonOb_node_format) +";"+"\n")
  
  edges_data = data[1]
  jsonOb_edges = json.dumps(edges_data)
  jsonOb_edges_format = format(jsonOb_edges)
  f.write("var edges = "+str(jsonOb_edges_format) +";"+"\n")
  
  heading_data = data[2]
  jsonOb_heading = json.dumps(heading_data)
  jsonOb_heading_format = format(jsonOb_heading)
  f.write("var heading = "+str(jsonOb_heading_format) +";"+"\n")

  height_data = data[3]
  jsonOb_height = json.dumps(height_data)
  jsonOb_height_format = format(jsonOb_height)
  f.write("var height = "+str(jsonOb_height_format) +";"+"\n")

  width_data = data[4]
  jsonOb_width = json.dumps(width_data)
  jsonOb_width_format = format(jsonOb_width)
  f.write("var width = "+str(jsonOb_width_format) +";"+"\n")

  options_data = data[5]
  jsonOb_options = json.dumps(options_data)
  jsonOb_options_format = format(jsonOb_options)
  f.write("var options = "+str(jsonOb_options_format) +";"+"\n")
  
  # G2.show('view.html')

 
  