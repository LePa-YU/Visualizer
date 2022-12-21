import json

def convertToHtml(data, file_name):
    file_html = open(file_name , "w")
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
    <script type="text/javascript"> 
     var nodeList = new vis.DataSet();
     var edgeList = new vis.DataSet();\n''')

    heading_data = data[2]
    jsonOb_heading = json.dumps(heading_data)
    jsonOb_heading_format = format(jsonOb_heading)
    file_html.write("\t\t var heading = "+str(jsonOb_heading_format) +";"+"\n")

    height_data = data[3]
    jsonOb_height = json.dumps(height_data)
    jsonOb_height_format = format(jsonOb_height)
    file_html.write("\t\t var height = "+str(jsonOb_height_format) +";"+"\n")

    width_data = data[4]
    jsonOb_width = json.dumps(width_data)
    jsonOb_width_format = format(jsonOb_width)
    file_html.write("\t\t var width = "+str(jsonOb_width_format) +";"+"\n")

    options_data = data[5]
    jsonOb_options = json.dumps(options_data)
    jsonOb_options_format = format(jsonOb_options)  
    file_html.write("\t\t var options = "+str(jsonOb_options_format) +";"+"\n\n")

    nodes_data = data[0]
    for n in nodes_data:
        jsonOb_node = json.dumps(n)
        jsonOb_node_format = format(jsonOb_node)
        file_html.write("\t\t nodeList.add("+str(jsonOb_node_format) +");"+"\n")
    file_html.write('''
     ''')
    edges_data = data[1]
    for e in edges_data:
        jsonOb_edges = json.dumps(e)
        jsonOb_edges_format = format(jsonOb_edges)
        file_html.write("\t\t edgeList.add("+str(jsonOb_edges_format) +");"+"\n")
    # add rest of the html
    file_html.write('''
   
    var container = document.getElementById('mynetwork');
    var data = {
        nodes: nodeList,
        edges: edgeList
    };
    var opt = JSON.parse(options);

  // document.getElementById("demo").innerHTML = typeof(opt);
    var network = new vis.Network(container, data, opt);
    network.setSize(width, height);

    network.on("selectNode", function (params) {
      if (params.nodes.length == 1) {
        if (network.isCluster(params.nodes[0]) == true) {
          network.openCluster(params.nodes[0]);
        }
        else{
            var v = params.nodes[0];
            // document.getElementById("demo").innerHTML = v;
            network.cluster(getC(v));
        }
      }

        //url opening
      var nodeId = params.nodes;
      var node = nodeList.get(nodeId)[0];
      var nodeUrl = node.url;
      if(nodeUrl != "nil"){
        var openUrl = Boolean(confirm("This node contains a link would like to open it?"));
        if(openUrl){
          window.open(nodeUrl); 
        }
      }
    });

    function getC(v){
      var clusterOptionsByData = {
          joinCondition: function (childOptions) {
            return childOptions.isPartOf == v || childOptions.id == v;
          },
          processProperties: function (clusterOptions, childNodes, childEdges){
            var node;
            for(let i = 0; i<childNodes.length; i++){
              n = childNodes[i];
              if(n.id == v){
                node = n;
                break;
              }
            }

            // document.getElementById("demo").innerHTML += node.id;

            clusterOptions.shape = node.shape;
            clusterOptions.label = node.label;
            clusterOptions.color = node.color;
            clusterOptions.size = node.size;
            return clusterOptions;
          }

        };

      return clusterOptionsByData;
    }

    </script>
    </body>
    </html>

    ''')
    # Saving the data into the HTML file
    file_html.close()  
    # G2.show('view.html')





#######################################
def convertToHtml_Legend(data):
    file_html = open("index_Legend.html", "w")
    # Adding the input data to the HTML file
    file_html.write('''
    <!DOCTYPE html>
    <html>
    <head>
        <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
        <style type="text/css">
            #mynetwork {
                width: 100%;
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


    # add rest of the html
    file_html.write('''
    
    var nodeList = new vis.DataSet();
    var x = 0; 
    var y = 0; 
    var step = 5; 
    for(let i = 0; i<nodes.length; i++){
        var n = nodes[i];
        var n_info = {
            id: n.id,
            title: n.title,
            label: n.label,
            x : n.x,
            y : n.y,
            color: n.color,
                size: n.size, 
                shape: n.shape,
                font: { face: "Monospace", align: "left" }
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
            arrows: e.arrows,
            label: e.label
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
    network.autoResize = false; 
    network.setSize(width, '200px');
    
       

    </script>
    </body>
    </html>''')
    # Saving the data into the HTML file
    file_html.close()  
    # G2.show('view.html')