# required imports
import networkx as nx
import pyvisToHtml
from pyvis.network import Network
import textwrap

# method  that convert networkx to pyvis
def convert_to_pyvis(G, file_name, bg, font_color,file_label, view, physics):

    # create pyvis network
    G2 = Network(height="750px", width="100%", bgcolor=bg, font_color=font_color, notebook=True, directed=True)
    G2.from_nx(G)
     # add networkx to pyvis network
    # print(physics)
    # if (physics):  
    #     G2.show_buttons()
  
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
    pyvisToHtml.convertToHtml(data, file_name, bg, file_label, view, physics)
