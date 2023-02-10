import networkx as nx
import pyvisToHtml
from pyvis.network import Network

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

  G.add_node(7, label = "Atomic iER       ", title="legend", shape = "text", color= general_node_color, x = 0, y = 150)
  G.add_node(0, label = "", title="legend", color= general_node_color, x = 100, y = 150)

  G.add_node(8, label = "Assesses", title="legend", shape = "text", color= general_node_color, x = 200, y = 0)
  G.add_node(9, label = " ",title="legend", shape="text", x = 250, y = 0)
  G.add_node(10, label = " ",title="legend", shape="text", x = 400, y = 0)
  G.add_edge(9, 10,color= assess_edge_color)
  
  G.add_node(11, label = "ComesAfter", title="legend", shape = "text", color= general_node_color, x = 200, y = 50)
  G.add_node(12, label = " ",title="legend", shape="text", x = 250, y = 50)
  G.add_node(13, label = " ",title="legend", shape="text", x = 400, y = 50)
  G.add_edge(12, 13,weight = 5, color= requires_edge_color)
 
  G.add_node(14, label = "isPartOf", title="legend", shape = "text", color= general_node_color, x = 200, y = 100)
  G.add_node(15, label = " ",title="legend", shape="text", x = 250, y = 100)
  G.add_node(16, label = " ",title="legend", shape="text", x = 400, y = 100)
  G.add_edge(15, 16, color = isPartOf_edge_color)

  G2 = Network(height="800px", width="100%", bgcolor="white", font_color="black", notebook=True,heading='', directed=True)
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
  G2.options.interaction = interaction
  data = G2.get_network_data()
  pyvisToHtml.convertToHtml_Legend(data)
  
  