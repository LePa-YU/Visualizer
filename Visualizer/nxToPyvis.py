# this class convert a given networkX to data and pass to pyvisToHtml.convertToHtml
# the length of node title are set here to 15

# required imports
import networkx as nx
import pyvisToHtml
from pyvis.network import Network
import textwrap

# method  that convert networkx to pyvis
def convert_to_pyvis(G, file_name, bg, font_color,file_label, view, physics, isHorizontal, download_dataset_only, csvRows, needsStabilization, select_edit_node_id, select_edit_node2_id, is_custom):

    # create pyvis network
    G2 = Network(height="750px", width="100%", bgcolor=bg, font_color=font_color, notebook=True, directed=True)
    # add networkx to pyvis network
    # if (physics):  G2.show_buttons()
    G2.from_nx(G)
  
    # wrap the long title aka node labels to fit in 15 character at each row
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
    pyvisToHtml.convertToHtml(data, file_name, bg, file_label, view, isHorizontal, download_dataset_only, csvRows, needsStabilization, physics, select_edit_node_id,  select_edit_node2_id, is_custom)
