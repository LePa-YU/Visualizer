import json

def convertToHtml(data, bg, fix):
    file_html = open("index.html", "w")
    # Adding the input data to the HTML file
    file_html.write('''
    <!DOCTYPE html>
    <html>
    <head>
        <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
        <style type="text/css">
            #mynetwork {
                width: 100%;
                height: 800px;
                border: 1px solid lightgray;
            }
        </style>
        <!-- <script src="network.js"></script> -->
        <script type="text/javascript" src="network.js"></script>
    </head>
    <body>
    <div id="mynetwork"></div>
    <div id="demo"></div>
    <!-- <script type="text/javascript" src="network.js"></script> -->
    <script type="text/javascript"> \n''')
    
    nodes_data = data[0]
    jsonOb_node = json.dumps(nodes_data)
    jsonOb_node_format = format(jsonOb_node)
    file_html.write("\t var nodes = "+str(jsonOb_node_format) +";"+"\n")

    edges_data = data[1]
    jsonOb_edges = json.dumps(edges_data)
    jsonOb_edges_format = format(jsonOb_edges)
    file_html.write("\t var edges = "+str(jsonOb_edges_format) +";"+"\n")

    heading_data = data[2]
    jsonOb_heading = json.dumps(heading_data)
    jsonOb_heading_format = format(jsonOb_heading)
    file_html.write("\t var heading = "+str(jsonOb_heading_format) +";"+"\n")

    height_data = data[3]
    jsonOb_height = json.dumps(height_data)
    jsonOb_height_format = format(jsonOb_height)
    file_html.write("\t var height = "+str(jsonOb_height_format) +";"+"\n")

    width_data = data[4]
    jsonOb_width = json.dumps(width_data)
    jsonOb_width_format = format(jsonOb_width)
    file_html.write("\t var width = "+str(jsonOb_width_format) +";"+"\n")

    options_data = data[5]
    jsonOb_options = json.dumps(options_data)
    jsonOb_options_format = format(jsonOb_options)  
    file_html.write("\t var options = "+str(jsonOb_options_format) +";"+"\n")

    # add bg color to js
    jsonOb_bg = json.dumps(bg)
    jsonOb_bg_format = format(jsonOb_bg)  
    file_html.write("\t var bgColor = "+str(jsonOb_bg_format) +";"+"\n")

    # # add fix to js
    # jsonOb_fix = json.dumps(fix)
    # jsonOb_fix_format = format(jsonOb_fix)  
    # file_html.write("\t var isFixed = "+str(jsonOb_fix_format) +";"+"\n")

    # add rest of the html
    file_html.write('''
    
    document.getElementById("mynetwork").style.background = bgColor; 
    var nodeList = new vis.DataSet();
    for(let i = 0; i<nodes.length; i++){
        var n = nodes[i];
        var n_info = {
            id: n.id,
            title: n.title,
            label: n.label,
            color: n.color,
                size: n.size, 
                shape: n.shape,
                font: n.font
            };
            nodeList.add(n_info);
        }
        
    var edgeList = new vis.DataSet();
    for(let i = 0; i<edges.length; i++){
        var e = edges[i];
        var e_info = {
            from: e.from, 
            to: e.to,
            color: e.color, 
            width: e.width,
            arrows: e.arrows
        };
         edgeList.add(e_info);
    }
    
    var container = document.getElementById('mynetwork');
    var data = {
        nodes: nodeList,
        edges: edgeList
    };
    var opt = JSON.parse(options);
    
    var network = new vis.Network(container, data, opt);
    network.setSize(width, height);
    
       

    </script>
    </body>
    </html>''')
    # Saving the data into the HTML file
    file_html.close()  
    # G2.show('view.html')