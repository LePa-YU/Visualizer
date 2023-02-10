# required imports
import networkx as nx
import pyvisToHtml
import nxToPyvis
import toolTip
from pyvis.network import Network
import pandas as pd
import textwrap

## this file contains code for different visualzation/ views of the LePa visualizer --> aka model

# this method set the data for different global attributes based on given dataframe each representing a column of the dataframe
def setData(df):
  # we set all column heading to lowercase
  df.columns = df.columns.str.lower()
  
  # all columns have try except clause. in case of missing column the attribute is assigned an empty value
  # note that rows accessed cannot be empty. if there is a possibility of them being empty then they should be set
  # to nil (check the data for alternative). 
  
  # precondition: node ID is an integer and this column cannot be empty in the dataset. 
  global df_id
  try:
    df_id = df['id']
  except:
    df['id'] =""
    df_id = df['id']

  #title is the name of the node that is displayed on the screen. this entry cannot be empty
  # value type: String
  global df_title
  try:
    df_title = df['title']
  except:
    df['title'] = ""
    df_title = df['title']

  # an alternative name/ title for the er
  #value type: String
  global df_alt
  try:
    df["alternative"].fillna("nil", inplace = True)
    df_alt = df['alternative']
  except:
    df['alternative']=""
    df_alt = df['alternative']

  # the target url of the ER if it exist. note that if there is none the field must be filled with nil to not cause problem 
  #in the computation later on.
  # value type: String 
  global df_tURL
  try:
    df['targeturl'].fillna("nil", inplace = True)
    df_tURL = df['targeturl']
  except:
    df['targeturl'] =""
    df_tURL = df['targeturl']

  # this field contains the type of ER. e.g. aER, iER, rER. if the ER is atomic then it include the file type for the atomic ER
  #value type: String
  global df_type
  try:
    df_type = df['type']
  except:
    df['type'] = ""
    df_type = df['type']

  # this field contains isPartOf relation of the current node with any other node in the dataset. 
  # value type: Integer
  global df_isPartOf
  try:
    df_isPartOf = df['ispartof']
  except:
    df['ispartof'] = ""
    df_isPartOf = df['ispartof']

  # this field contains assesses relation of the current node with any other node in the dataset. 
  # Value type: Integer
  global df_assesses
  try:
    df_assesses = df['assesses']
  except:
    df['assesses'] = ""
    df_assesses = df['assesses']
  
   # this field contains requires relation of the current node with any other node in the dataset. 
  # Value type: Integer
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

  # combine columns so each row represent one node
  # the tuple order(id, title, alteranteive name, url, type, isPArtyof, assesses, requires, comesAfter)
  global data_ER
  data_ER_zip = zip(df_id, df_title, df_alt, df_tURL, df_type, df_isPartOf, df_assesses, df_requires, df_comesAfter) # making tuples 
  data_ER = list(data_ER_zip)

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
#######################################################################
# this method create the content for the tooltip
def getToolTip(d_id, d_title, d_isPartOf, d_url):
  data_zip = zip(df_id, df_type, df_assesses)
  data_list = list(data_zip)
  toolTip.setData(data_list)
  text = toolTip.getToolTip(d_id, d_title, d_isPartOf, d_url)
  return text
#########################################################################
# comesAfter relationships
#1. regular comesAfter
def create_comesAfter_relationship(G, d_id, comeaAFter_id):
  try:
      d_comesAfter = int(comeaAFter_id)
  except:
      d_comesAfter = ""

  data_ca = zip(df_id)
  for d2 in data_ca:
    d2_id = d2[0]
    if(d_comesAfter == d2_id):
        #use label to label the edges
      G.add_edge( d2_id, d_id, weight = 5, color= requires_edge_color)

#2. Summative Assessment only view
def create_comesAfter_relationship_SA(G, d_id, d_type, comeaAFter_id):
    try:
      d_comesAfter = int(comeaAFter_id)
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
#########################################################################
#Assesses relationship:
def create_assesses_relationship(G, d_id, d_assesses):
  # finds the node that this node assesses
  data_assess = zip(df_id)
  for d1 in data_assess:
    d1_id = d1[0]
    if(d_assesses == d1_id):
      G.add_edge(d_id, d1_id, color= assess_edge_color)
#########################################################################
def create_ispartof_relationship(G, current_id, current_isPartOf):
  data_isPartOf = zip(df_id)
  for d in data_isPartOf:
    d_id = d[0]
    if(current_isPartOf == d_id):     
      G.add_edge( d_id,current_id, color = isPartOf_edge_color)
#########################################################################
# All ERs View
def All_ERs(dataframe, bg, file_label, view):
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
    try:
      d_assesses = int(d[6])
    except:
      d_assesses = ""
    
    if(d_type=="aER"):
      G.add_node(d_id, label = d_title, title=d_alt, shape="box", color= aER_node_color, url = d_url)
    elif(d_type == "rER"):
      G.add_node(d_id, label = d_title, title=d_alt, shape="triangle", color = rER_node_color, url = d_url) 
    elif(d_type == "iER"):
      G.add_node(d_id, label = d_title, title=d_alt, shape="circle", color= iER_node_color, url = d_url)
    #start and end nodes that are fixed position to represent the start and end of a course
    elif(d_type == "start"):
      G.add_node(d_id, label = d_title, title=d_alt, shape="diamond", color= iER_node_color, size=20, x = -1000, y=0, fixed = True, url = d_url)
    elif(d_type == "end"):
      G.add_node(d_id, label = d_title, title=d_alt, shape="diamond", color= iER_node_color, size=20, x = 1000, y = 0, fixed = True, url = d_url)
    # any entitiy that is not part of above aka atomic ERs. these can be part of isPartOf relationship. therefore isPartOf attribute is added
    # to their attributes to be used for the collapsibility of the nodes that have the same relationship with a particualr node
    else:
      toolTip = getToolTip(d_id, d_title, d_isPartOf, d_url)
      G.add_node(d_id, label = d_title, title=toolTip, color= general_node_color, isPartOf=d_isPartOf, url = d_url)
        
    ## relationship assesses if it exists:
    create_assesses_relationship(G, d_id, d_assesses)

    ## relationship comesAfter:
    create_comesAfter_relationship(G, d_id, d[8])

    ## relationship isPartOf:
    create_ispartof_relationship(G, d_id, d_isPartOf)
  
  # assign a file name
  file_name = "All_ERs.html"
  #convert the network to pyvis
  font_color = setFontColor(bg)
  nxToPyvis.convert_to_pyvis(G, file_name, bg, font_color ,file_label, view)

########################################################################    
# this method visualizes the course overview view which contains aER, rER, iER
def Course_Overview(dataframe, bg, file_label, view):
  setData(dataframe)
  G = nx.DiGraph()
  for d in data_ER:  
    d_id = d[0]
    d_title = d[1]
    d_type = d[4]
    d_alt = d[2]
    d_url = d[3]
    try:
      d_assesses = int(d[6])
    except:
      d_assesses = ""
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
    create_assesses_relationship(G, d_id, d_assesses)
    
    ## relationship comesAfter:
    create_comesAfter_relationship(G, d_id, d[8])
  
  file_name = "Course_Overview.html"
  font_color = setFontColor(bg)
  nxToPyvis.convert_to_pyvis(G, file_name, bg, font_color ,file_label, view)

##########################################################
########################################################################    
# this method visualizes the summative assessment only view which contains aER and their rER
def Summative_assessment_only(dataframe, bg, file_label, view):
  # set data from the input csv file
  setData(dataframe)
  # create networkx graph
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
    create_assesses_relationship(G, d_id, d_assesses)

    ## relationship comesAfter:
    create_comesAfter_relationship_SA(G, d_id, d_type, d[8])
  
  file_name = "Summative_assessment_only.html"
  font_color = setFontColor(bg)
  nxToPyvis.convert_to_pyvis(G, file_name, bg, font_color ,file_label, view)

########################################################################    
