# required imports
import networkx as nx
import pyvisToHtml
from pyvis.network import Network
import textwrap


# initial options
layout = {
    "randomSeed":10, 
    "improvedLayout": True, 
    "clusterThreshold":10,
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

# method  that convert networkx to pyvis
def convert_to_pyvis(G, file_name, bg, font_color,file_label, view):

    # create pyvis network
    G2 = Network(height="750px", width="100%", bgcolor=bg, font_color=font_color, notebook=True, directed=True)
    # add networkx to pyvis network
    G2.from_nx(G)

    # add individual options
    G2.options.edges = edges
    G2.options.nodes = nodes
    G2.options.interaction = interaction
    G2.options.manipulation = manipulation
    G2.options.layout = layout
  
    # wrap the long title aka node labels to fit in 15
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

    # getting the data from pyvis network to be used in vis.js
    data = G2.get_network_data()

  # the data is used to create an html file, args: data(network infor)/ file_name(name of the html file)/ bg(background selected by user-initially white)
    pyvisToHtml.convertToHtml(data, file_name, bg, file_label, view)
