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
    #col1
    G.add_node(1, label = "Activity ER      ", shape = "text", title="legend", color= self.colors.aER_node_color, x = 0, y = 0)
    G.add_node(2, label = "       ", shape="box", title="legend", color= self.colors.aER_node_color, x = 190, y = 0)
    
    G.add_node(3, label = "Rubric ER        ", shape="text", title="legend", color = self.colors.rER_node_color, x = 0, y = 50 )
    G.add_node(4, label = "", shape="triangle", title="legend", color = self.colors.rER_node_color, x = 190, y = 50 ) 

    G.add_node(5, label = "Instructional ER ", shape="text", title="legend", color= self.colors.iER_node_color, x = 0, y = 100)
    G.add_node(6, label = "    ", shape="circle", title="legend", color= self.colors.iER_node_color, x = 190, y = 100)

    G.add_node(8, label = "Assesses relation", title="legend", shape = "text", color= self.colors.assess_relationship_color, x = 0, y = 150)
    G.add_node(9, label = " ",title="legend", shape="text", x = 140, y = 150)
    G.add_node(10, label = " ",title="legend", shape="text", x = 240, y = 150)
    G.add_edge(9, 10,color= self.colors.assess_relationship_color)
    
    G.add_node(11, label = "    Comes Before relation", title="legend", shape = "text", color= self.colors.comesAfter_relationship_color, x = 0, y = 200)
    G.add_node(12, label = " ",title="legend", shape="text", x = 140, y = 200)
    G.add_node(13, label = " ",title="legend", shape="text", x = 240, y = 200)
    G.add_edge(12, 13,weight = 5, color= self.colors.comesAfter_relationship_color)
  
    G.add_node(14, label = "  is Part Of relation", title="legend", shape = "text", color= self.colors.isPartOf_relationship_color, x = 0, y = 250)
    G.add_node(15, label = " ",title="legend", shape="text", x = 140, y = 250)
    G.add_node(16, label = " ",title="legend", shape="text", x = 240, y = 250)
    G.add_edge(15, 16, color = self.colors.isPartOf_relationship_color)
    
    G.add_node(17, label = "      is Required By relation", title="legend", shape = "text", color= self.colors.requires_node_color, x = 0, y = 300)
    G.add_node(18, label = " ",title="legend", shape="text", x = 140, y = 300)
    G.add_node(19, label = " ",title="legend", shape="text", x = 240, y = 300)
    G.add_edge(18, 19, weight = 5, color = self.colors.requires_node_color)


   
    #col2
    G.add_node(20, label = "Atomic ER: images", title="legend", shape = "text", color= self.colors.atomic_node_color_img, x = 400, y = 0)
    G.add_node(21, label = "", title="legend", color= self.colors.atomic_node_color_img, x = 520, y = 0)

    G.add_node(22, label = "Atomic ER: Videos", title="legend", shape = "text", color= self.colors.atomic_node_color_mov, x = 400, y = 50)
    G.add_node(23, label = "", title="legend", color= self.colors.atomic_node_color_mov, x = 520, y = 50)

    G.add_node(24, label = "  Atomic ER: Software", title="legend", shape = "text", color= self.colors.atomic_node_color_software, x = 400, y = 100)
    G.add_node(25, label = "", title="legend", color= self.colors.atomic_node_color_software, x = 520, y = 100)

    G.add_node(26, label = "Atomic ER: Audio ", title="legend", shape = "text", color= self.colors.atomic_node_color_audio, x = 400, y = 150)
    G.add_node(27, label = "", title="legend", color= self.colors.atomic_node_color_audio, x = 520, y = 150)

    G.add_node(7, label = "    Atomic ER: collection", title="legend", shape = "text", color= self.colors.atomic_node_color_coll, x = 400, y = 200)
    G.add_node(0, label = "", title="legend", color= self.colors.atomic_node_color_coll, x = 520, y = 200)

    G.add_node(28, label = "Atomic ER: Text  ", title="legend", shape = "text", color= self.colors.atomic_node_color_text, x = 400, y = 250)
    G.add_node(29, label = "", title="legend", color= self.colors.atomic_node_color_text, x = 520, y = 250)
    
    G.add_node(30, label = "Atomic ER: Dataset", title="legend", shape = "text", color= self.colors.atomic_node_color_dataset, x = 400, y = 300)
    G.add_node(31, label = "", title="legend", color= self.colors.atomic_node_color_dataset, x = 520, y = 300)
    