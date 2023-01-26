# required imports
import networkx as nx
import pyvisToHtml
from pyvis.network import Network
import pandas as pd
import streamlit as st
import textwrap
import sys

## this file contains code for different visualzation/ views of the LePa visualizer --> aka model

# this method set the data for different global attributes based on given dataframe each representing a column of the dataframe
def setData(df):
  # we set all column heading to lowercase
  df.columns = df.columns.str.lower()
  
  # all columns have try except clause. in case of missing column the attribute is assigned an empty value
  # note that rows accessed cannot be empty. if there is a possibility of them being empty then they should be set
  # to nil
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
  
  # this relationship is used to show Chronological order of the ERs
  global df_comesAfter
  try:
    df_comesAfter = df['comesafter']
  except:
    df['comesafter']=""
    df_comesAfter = df['comesafter']

 # this is  used for summative assessment only relationship
  try:
    df_comesAfter_aER = df["comesafter_aer"]
  except:
    df["comesafter_aer"]=""
    df_comesAfter_aER = df["comesafter_aer"]
  
  # combine columns so each row represent one node 
  global data_ER
  data_ER = zip(df_id, df_title, df_alt, df_tURL, df_type, df_isPartOf, df_assesses, df_requires, df_comesAfter, df_comesAfter_aER) # making tuples 

# initial options
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
def convert_to_pyvis(G, file_name, bg):
  G2 = Network(height="800px", width="100%", bgcolor=bg, font_color=setFontColor(bg), notebook=True,heading='', directed=True)
  G2.from_nx(G)
  G2.options.edges = edges
  G2.options.nodes = nodes
  G2.options.interaction = interaction
  G2.options.manipulation = manipulation
  G2.options.layout = layout
  
  for node in G2.nodes:
    id_string = node["label"]
    width = 15
    try:
      wrapped_strings = textwrap.wrap(id_string, width)
      wrapped_id =""; 
      for line in wrapped_strings:
        wrapped_id = textwrap.fill(id_string, width)
      node["label"] = wrapped_id
    except:
      node["label"] = id_string

  data = G2.get_network_data()

  # the data is used to create an html file, args: data(network infor)/ file_name(name of the html file)/ bg(background selected by user-initially white)
  pyvisToHtml.convertToHtml(data, file_name, bg)

#########################################################################

# this method set the colors for different entities of the network
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

#this methods set the font color based on the bg (String). if bg is white --> font is black else font is white
def setFontColor(bg):
  # set font color based on bg:
  font_color = ""
  if(bg=="white"):
    font_color = "black"
  else:
    font_color = "white"
  return font_color
 
#########################################################################
# All ERs View
def All_ERs(dataframe, bg):
  setData(dataframe)
  G = nx.DiGraph()
  for d in data_ER:
    d_id = d[0]
    d_title = d[1]
    d_type = d[4]
    d_alt = d[2]
    d_url = d[3]
    try:
      d_isPartOf = int(d[5])
    except:
      d_isPartOf = ""
    if(d_type=="aER"):
      G.add_node(d_id, label = d_title, shape="box", title=d_alt, color= aER_node_color, url = d_url)
    elif(d_type == "rER"):
      G.add_node(d_id, label = d_title, shape="triangle", title=d_alt, color = rER_node_color, url = d_url) 
    elif(d_type == "iER"):
      G.add_node(d_id, label = d_title, shape="circle", title=d_alt, color= iER_node_color, url = d_url)
    #start and end nodes that are fixed position to represent the start and end of a course
    elif(d_type == "start"):
      G.add_node(d_id, label = d_title, shape="diamond", title=d_alt, color= iER_node_color, size=20, x = -1000, y=0, fixed = True, url = d_url)
    elif(d_type == "end"):
      G.add_node(d_id, label = d_title, shape="diamond", title=d_alt, color= iER_node_color, size=20, x = 1000, y = 0, fixed = True, url = d_url)
    # any entitiy that is not part of above. these can be part of isPartOf relationship. therefore isPartOf attribute is added
    # to their attributes to be used for the collapsibility of the nodes that have the same relationship with a particualr node
    else:
      G.add_node(d_id, label = d_title, title=d_alt, color= general_node_color, isPartOf=d_isPartOf, url = d_url)
        
    ## relationship assesses if it exists:
    try:
      d_assesses = int(d[6])
    except:
      d_assesses = ""
    # finds the node that this node assesses
    data_assess = zip(df_id)
    for d1 in data_assess:
      d1_id = d1[0]
      if(d_assesses == d1_id):
        G.add_edge(d_id, d1_id, color= assess_edge_color)
        
    ## relationship requires:
    # d_requires = d[7]
    # data_req = zip(df_id)
    # for d2 in data_req:
    #   d2_id = d2[0]
    #   if(d_requires == d2_id):
    #     #use label to label the edges
    #     G.add_edge( d2_id, d_id, weight = 5, color= requires_edge_color)

    ## relationship comesAfter:
    try:
      d_comesAfter = int(d[8])
    except:
      d_comesAfter = ""

    data_ca = zip(df_id)
    for d2 in data_ca:
      d2_id = d2[0]
      if(d_comesAfter == d2_id):
        #use label to label the edges
        G.add_edge( d2_id, d_id, weight = 5, color= requires_edge_color)

    ## relationship isPartOf:
    data_isPartOf = zip(df_id)
    for d3 in data_isPartOf:
      d3_id = d3[0]
      if(d_isPartOf == d3_id):     
        G.add_edge( d3_id,d_id, color = isPartOf_edge_color)
  
  # assign a file name
  file_name = "All_ERs.html"
  #convert the network to pyvis
  convert_to_pyvis(G, file_name, bg)

########################################################################    
# this method visualizes the course overview view which contains aER, rER, iER
def Course_Overview(dataframe, bg):
  setData(dataframe)
  G = nx.DiGraph()
  for d in data_ER:  
    d_id = d[0]
    d_title = d[1]
    d_type = d[4]
    d_alt = d[2]
    d_url = d[3]
    if(d_type=="aER"):
      G.add_node(d_id, label = d_title, shape="box", title=d_alt, color = aER_node_color, url = d_url)
    elif(d_type == "rER"):
      G.add_node(d_id, label = d_title, shape="triangle", title=d_alt, color = rER_node_color, url = d_url) 
    elif(d_type == "iER"):
      G.add_node(d_id, label = d_title, shape="circle", title=d_alt, color= iER_node_color, url = d_url)
    elif(d_type == "start"):
      G.add_node(d_id, label = d_title, shape="diamond", title=d_alt, color= iER_node_color, size=20, x = -1000, y=0, fixed = True, url = d_url)
    elif(d_type == "end"):
      G.add_node(d_id, label = d_title, shape="diamond", title=d_alt, color= iER_node_color, size=20, x = 1000, y = 0, fixed = True, url = d_url)
        
    ## relationship assesses:
    try:
      d_assesses = int(d[6])
    except:
      d_assesses = ""
    data_assess = zip(df_id)
    for d1 in data_assess:
      d1_id = d1[0]
      if(d_assesses == d1_id):
        G.add_edge(d_id, d1_id, color= assess_edge_color)
    
    ## relationship comesAfter:
    try:
      d_comesAfter = d[8]
    except:
      d_comesAfter = ""
    data_ca = zip(df_id)
    for d2 in data_ca:
      d2_id = d2[0]
      if(d_comesAfter == d2_id):
        #use label to label the edges
        G.add_edge( d2_id, d_id, weight = 5, color= requires_edge_color)
  
  file_name = "Course_Overview.html"
  convert_to_pyvis(G,file_name, bg)

##########################################################
########################################################################    
# this method visualizes the summative assessment only view which contains aER and their rER
def Summative_assessment_only(dataframe, bg):
  setData(dataframe)
  G = nx.DiGraph()
  for d in data_ER:
    d_id = d[0]
    d_title = d[1]
    d_type = d[4]
    d_alt = d[2]
    d_url = d[3]
    if(d_type=="aER"):
      G.add_node(d_id, label = d_title, shape="box", title=d_alt, color= aER_node_color, url = d_url)
    elif(d_type == "rER"):
      G.add_node(d_id, label = d_title, shape="triangle", title=d_alt, color = rER_node_color, url = d_url) 
    elif(d_type == "start"):
      G.add_node(d_id, label = d_title, shape="diamond", title=d_alt, color= iER_node_color, size=20, x = -1000, y=0, fixed = True, url = d_url)
    elif(d_type == "end"):
      G.add_node(d_id, label = d_title, shape="diamond", title=d_alt, color= iER_node_color, size=20, x = 1000, y = 0, fixed = True, url = d_url)
   
    ## relationship assesses:
    try:
      d_assesses = int(d[6])
    except:
      d_assesses = ""
    data_assess = zip(df_id)
    for d1 in data_assess:
      d1_id = d1[0]
      if(d_assesses == d1_id):
        G.add_edge(d_id, d1_id, color= assess_edge_color)

    ## relationship comesAfter:
    try:
      d_comesAfter = d[8]
    except:
      d_comesAfter = ""
    data_ca = zip(df_id, df_type, df_comesAfter)
    data_list = list(data_ca)
    i = 0; 
    while i< len(data_list):
      d1_id = data_list[i][0]
      if(d_comesAfter == d1_id):
        d1_type = data_list[i][1]
        d1_comesAfter = data_list[i][2]
        if((d1_type == "aER" and d_type == "aER") or d_type == "end"):
          G.add_edge( d1_id, d_id, weight = 5, color= requires_edge_color)
        elif(d1_type == "iER"):
          j = i
          while j > -1:
            d2_id = data_list[j][0]
            d2_type = data_list[j][1]
            if(d1_comesAfter == d2_id):
              if(d2_type == "iER"):
                d1_comesAfter = data_list[j][2]
                j = i
              elif((d2_type == "aER" or d2_type =="start") and d_type =="aER"):
                G.add_edge( d2_id, d_id, weight = 5, color= requires_edge_color)
              
            j = j -1

      i = i +1
  
  file_name = "Summative_assessment_only.html"
  convert_to_pyvis(G,file_name, bg)

########################################################################    
# the legend is created manually but corresponds to the colors of entities
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
  
  