import json

def convertToHtml(data, file_name, bg, file_label, view, isHorizontal):
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
            #canvas {
                width: 100%;
                height: 700px;
            }
            #labelContainer {
                width: 100%; 
                height: 20px; 
                text-align: right; 
            }
            #label {
                padding-right: 1%; 
            }
        </style>
        <!-- <script src="network.js"></script> -->
        <script type="text/javascript" src="network.js"></script>
    </head>
    <body>
    <div id="mynetwork">
      <div id="labelContainer"><p id="label"></p></div> 
      <div id="canvas"></div>
    </div>
    <!-- <script type="text/javascript" src="network.js"></script> -->
    <script type="text/javascript"> 
       window.onload=function(){
    var mobile = (/iphone|ipad|ipod|android|blackberry|mini|windows\sce|palm/i.test(navigator.userAgent.toLowerCase()));
    if (mobile) {
       alert("For the best viewing experience, please use a PC");           
    } 
    }
     var nodeList = new vis.DataSet();
     var edgeList = new vis.DataSet();\n''')

    # file label 
    jsonOb_file_label = json.dumps(file_label)
    jsonOb_file_label_format = format(jsonOb_file_label)
    file_html.write("\t\t var fileLabel = "+str(jsonOb_file_label_format) +";"+"\n")

    #view name
    jsonOb_view = json.dumps(view)
    jsonOb_view_format = format(jsonOb_view)
    file_html.write("\t\t var view = "+str(jsonOb_view_format) +";"+"\n")

    # heading from the network
    heading_data = data[2]
    jsonOb_heading = json.dumps(heading_data)
    jsonOb_heading_format = format(jsonOb_heading)
    file_html.write("\t\t var heading = "+str(jsonOb_heading_format) +";"+"\n")

    # height of network
    height_data = data[3]
    jsonOb_height = json.dumps(height_data)
    jsonOb_height_format = format(jsonOb_height)
    file_html.write("\t\t var height = "+str(jsonOb_height_format) +";"+"\n")

    #width of the network
    width_data = data[4]
    jsonOb_width = json.dumps(width_data)
    jsonOb_width_format = format(jsonOb_width)
    file_html.write("\t\t var width = "+str(jsonOb_width_format) +";"+"\n")

    #network options such as nodes, edge, interaction, physics, etc. 
    options_data = data[5]
    jsonOb_options = json.dumps(options_data)
    jsonOb_options_format = format(jsonOb_options)  
    file_html.write("\t\t var options = "+str(jsonOb_options_format) +";"+"\n\n")
 
    #horizontal or vertical layout
    jsonOb_isHorizontal = json.dumps(isHorizontal)
    jsonOb_isHorizontal_format = format(jsonOb_isHorizontal)  
    file_html.write("\t\t var isHorizontal = "+str(jsonOb_isHorizontal_format) +";"+"\n\n")

    # background data
    jsonOb_bg = json.dumps(bg)
    jsonOb_bg_format = format(jsonOb_bg)  
    file_html.write("\t\t var bg = "+str(jsonOb_bg_format) +";"+"\n")
    file_html.write('''
        document.getElementById('mynetwork').style.background = bg; 
     ''')

    # nodes data from network
    nodes_data = data[0]
    for n in nodes_data:
        jsonOb_node = json.dumps(n)
        jsonOb_node_format = format(jsonOb_node)
        file_html.write("\t\t nodeList.add("+str(jsonOb_node_format) +");"+"\n")
    file_html.write('''
     ''')
    
    #edge data from network
    edges_data = data[1]
    for e in edges_data:
        jsonOb_edges = json.dumps(e)
        jsonOb_edges_format = format(jsonOb_edges)
        file_html.write("\t\t edgeList.add("+str(jsonOb_edges_format) +");"+"\n")
    
    # add rest of the html
    file_html.write('''
    document.getElementById("label").innerHTML = fileLabel +" (" + view + ")";
    if(bg == "black"){
      document.getElementById("label").style.color = 'white';
    }
    var container = document.getElementById('canvas');
    // creating the data to be used for visuaization
    var data = {
        nodes: nodeList,
        edges: edgeList
    };
   //options:
      var options = {
		nodes: {
			borderWidth: 3,
			borderWidthSelected: 6,
			shadow: {
				enabled: true,
				color: "white",
				size: 9,
				x: -1,
				y: -2
			},
			shapeProperties: {
				useBorderWithImage: true
			}
		},
		edges: {
    		color: {
      			inherit: true
    		},
    		dashes: true,
    		font: {
      			strokeWidth: 5
    		},
    		hoverWidth: 3.2,
    	},
		interaction: {
     		hideEdgesOnZoom: true,
     		hover: true,
     		keyboard: {
       			enabled: true
     		},
     		multiselect: true,
     		navigationButtons: true
		},
		manipulation: {
			enabled: true
		},
		layout: {
    		randomSeed:10, 
    		improvedLayout: false, 
    		clusterThreshold:150,
  		},
		physics: {
			barnesHut: {
				centralGravity: 0,
				springLength: 140,
				springConstant: 1
        
			},
			minVelocity: 0.75,
      stabilization:{
        enabled: true, 
        iterations: 800
      }
		}

	}
    //creating the vis network
    var network = new vis.Network(container, data, options);
    network.setSize(width, height);
    network.once("beforeDrawing", function () {
      if(isHorizontal){
        network.focus(0, {
          scale: 0.5,
          offset: {x:-300, y:0}
        });
      }
      else{
        network.focus(0, {
          scale: 0.5,
          offset: {x:0, y:-300}
        });
      }
    }); 
    // node collapse. if only one node is selected if the node is clustred (collapsed) then the cluster is open
    // else the node is collapsed if if they have the isPartOf relation corresponding to this node's id (var v)
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
      
        //url opening
      nodeId = params.nodes;
      node = nodeList.get(nodeId)[0];
      nodeUrl = node.url;
        //using eventlistener and event.key we can specify keys to open a link when a node is selected
      document.addEventListener("keypress", (event)=>
      {
				  if(!(nodeUrl === "nan" ) && event.key == "Enter")
          {
					  window.open(nodeUrl);
            delete nodeUrl;  
				  }
			}); 
        
      
      }

        
    });

    network.on('stabilized', function(params) {
      console.log(params); 
    });

    // cluster/ collapse options based on isPartOf. this method returns the cluster options to be used for the clustering
    function getC(v){
      var clusterOptionsByData = {
          // condition for clustering: nodes with ispartof same as v and node that has id v
          joinCondition: function (childOptions) {
            return childOptions.isPartOf == v || childOptions.id == v;
          },
          // to have the clusters inherit the properties of the selected node
          processProperties: function (clusterOptions, childNodes, childEdges){
            var node;
            // find the node with id v
            for(let i = 0; i<childNodes.length; i++){
              n = childNodes[i];
              if(n.id == v){
                node = n;
                break;
              }
            }

            // document.getElementById("demo").innerHTML += node.id;
            // adding the properties of the node to th cluster options
            clusterOptions.shape = node.shape;
            clusterOptions.label = node.label;
            clusterOptions.color = node.color;
            clusterOptions.size = node.size;
            clusterOptions.font = node.font; 
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
def convertToHtml_Legend(data, bg):
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
                height: 300px; 
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

     # background data
    jsonOb_bg = json.dumps(bg)
    jsonOb_bg_format = format(jsonOb_bg)  
    file_html.write("\t\t var bg = "+str(jsonOb_bg_format) +";"+"\n")
    file_html.write('''
        document.getElementById('mynetwork').style.background = bg; 
     ''')

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
                font: {face: "Monospace", align: "left", color: n.font.color }
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
    network.setSize(width, '300px');
    
       

    </script>
    </body>
    </html>''')
    # Saving the data into the HTML file
    file_html.close()  
    # G2.show('view.html')