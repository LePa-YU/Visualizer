import networkx as nx
import pyvisToHtml
from pyvis.network import Network

class Legend:

  def setColors(self, colors):
    self.colors = colors

  def create_legend(self, bg, font_color):
    G = nx.DiGraph()
    Legend.__addNodes(self, G)
    G2 = Network(height="800px", width="100%", font_color= font_color, notebook=True,heading='', directed=True)
    G2.from_nx(G)
    Legend.__setOptions(self, G2)
    data = G2.get_network_data()
    pyvisToHtml.convertToHtml_Legend(data, bg)

  def __setOptions(self, G2):
    edges = {
      "color": {"inherit": True},
      "dashes": True,
      "font": {"strokeWidth": 5},
      "hoverWidth": 3.2,
      "scaling": {"label": {"min": 24}},
      "selfReference": {"angle": 0.7853981633974483},
      "smooth": {"roundness": 0.7}
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
      "shapeProperties": {"borderRadius": 4},
      "fixed": {"x": True, "y": True}
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

  def __addNodes(self, G):
    G.add_node(1, label = "Activity ER      ", shape = "text", title="legend", color= self.colors.aER_node_color, x = 0, y = 0)
    G.add_node(2, label = "       ", shape="box", title="legend", color= self.colors.aER_node_color, x = 100, y = 0)
    
    G.add_node(3, label = "Rubric ER        ", shape="text", title="legend", color = self.colors.rER_node_color, x = 0, y = 50 )
    G.add_node(4, label = "", shape="triangle", title="legend", color = self.colors.rER_node_color, x = 100, y = 50 ) 

    G.add_node(5, label = "Instructional ER ", shape="text", title="legend", color= self.colors.iER_node_color, x = 0, y = 100)
    G.add_node(6, label = "    ", shape="circle", title="legend", color= self.colors.iER_node_color, x = 100, y = 100)

    G.add_node(7, label = "Atomic iER       ", title="legend", shape = "text", color= self.colors.atomic_node_color, x = 0, y = 150)
    G.add_node(0, label = "", title="legend", color= self.colors.atomic_node_color, x = 100, y = 150)

    G.add_node(8, label = "Assesses", title="legend", shape = "text", color= self.colors.assess_relationship_color, x = 200, y = 0)
    G.add_node(9, label = " ",title="legend", shape="text", x = 260, y = 0)
    G.add_node(10, label = " ",title="legend", shape="text", x = 400, y = 0)
    G.add_edge(9, 10,color= self.colors.assess_relationship_color)
    
    G.add_node(11, label = "  ComesAfter", title="legend", shape = "text", color= self.colors.comesAfter_relationship_color, x = 200, y = 50)
    G.add_node(12, label = " ",title="legend", shape="text", x = 260, y = 50)
    G.add_node(13, label = " ",title="legend", shape="text", x = 400, y = 50)
    G.add_edge(12, 13,weight = 5, color= self.colors.comesAfter_relationship_color)
  
    G.add_node(14, label = "isPartOf", title="legend", shape = "text", color= self.colors.isPartOf_relationship_color, x = 200, y = 100)
    G.add_node(15, label = " ",title="legend", shape="text", x = 260, y = 100)
    G.add_node(16, label = " ",title="legend", shape="text", x = 400, y = 100)
    G.add_edge(15, 16, color = self.colors.isPartOf_relationship_color)
