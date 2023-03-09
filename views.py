from csv import reader
import networkx as nx
import pyvisToHtml
import nxToPyvis
import node
import colors
import csv


class Views:
    def __init__(self, dataCSV):
        # self.data = dataCSV.to_records(index=False).tolist()
        dataCSV.columns = dataCSV.columns.str.lower()
        self.data = dataCSV.to_dict('records')

        self.nodeList=[]
        for er in self.data:
            er_node = node.Node(er)
            self.nodeList.append(er_node)

    
    def Summative_assessment_only(self, bg, font_color, file_label, view):
        # create networkx graph
        G = nx.DiGraph()
        # aER = true, rER = true, iER = false, atomicER=false
        Views.__addNodes(self, G, True, True, False, False)
        Views.__create_assesses_relationship(self, G)
        Views. __create_comesAfter_relationship_SA(self, G)
       

        # assign a file name
        file_name = "Summative_assessment_only.html"
        #convert the network to pyvis
        nxToPyvis.convert_to_pyvis(G, file_name, bg, font_color ,file_label, view)
    
    def Course_Overview(self, bg,font_color, file_label, view):
        # create networkx graph
        G = nx.DiGraph()
        #aER = true, rER = true, iER = false, atomicER=false
        Views.__addNodes(self, G, True, True, True, False)
        Views.__create_assesses_relationship(self, G)
        Views. __create_comesAfter_relationship(self, G)
        # assign a file name
        file_name = "Course_Overview.html"
        #convert the network to pyvis
        nxToPyvis.convert_to_pyvis(G, file_name, bg, font_color ,file_label, view)

    def  All_ERs(self, bg,font_color, file_label, view):
        # create networkx graph
        G = nx.DiGraph()
        #aER = true, rER = true, iER = true, atomicER=true
        Views.__addNodes(self, G, True, True, True, True)
        Views.__create_assesses_relationship(self, G)
        Views. __create_comesAfter_relationship(self, G)
        Views. __create_isPartOf_relationship(self, G)
        # assign a file name
        file_name = "All_ERs.html"
        #convert the network to pyvis
        nxToPyvis.convert_to_pyvis(G, file_name, bg, font_color ,file_label, view)
    
    def Requirements(self, bg,font_color, file_label, view):
         # create networkx graph
        G = nx.DiGraph()
        #aER = true, rER = true, iER = true, atomicER=true
        Views.__addNodes(self, G, True, True, True, True)
        Views.__create_assesses_relationship(self, G)
        Views. __create_comesAfter_relationship(self, G)
        Views. __create_isPartOf_relationship(self, G)
        Views.__create_requires_relationshipAll(self, G, True)
        # assign a file name
        file_name = "requirements.html"
        #convert the network to pyvis
        nxToPyvis.convert_to_pyvis(G, file_name, bg, font_color ,file_label, view)

    def setColors(self, aER_node_color, rER_node_color, iER_node_color,  general_node_color, assess_edge_color, requires_edge_color, isPartOf_edge_color, start_node, end_node, requires_node):
        self.all_colors = colors.Color(aER_node_color, rER_node_color, iER_node_color,  general_node_color, assess_edge_color, requires_edge_color, isPartOf_edge_color, start_node, end_node, requires_node)

    def getColors(self):
        return self.all_colors

    def __addNodes(self, G, has_aER, has_rER, has_iER, has_atomicER):
        start_position= Views.__get_position(self)
        end_position = - start_position
        position = start_position + 450
        rER_position = 50

        for node in self.nodeList:
            node_type = node.er_type
            if(node_type == "start"):
                G.add_node(node.er_id, label = node.er_title, title=node.er_alternative, shape="diamond", color= self.all_colors.start_node_color,size=20, x = start_position, y=0, fixed = True, url = str(node.er_url))
            elif(node_type == "end"):
                G.add_node(node.er_id, label = node.er_title, title=node.er_alternative, shape="diamond", color= self.all_colors.end_node_color,size=20, x = end_position, y=0, fixed = True, url = str(node.er_url))
            elif(node_type =="aER" and has_aER):
                # G.add_node(node.er_id, label = node.er_title, title=node.er_alternative, shape="box", color= self.all_colors.aER_node_color, url = str(node.er_url))
                G.add_node(node.er_id, label = node.er_title, title=node.er_alternative, shape="box", color= self.all_colors.aER_node_color,x = position, y=0, url = str(node.er_url))
                position = position+450
            elif(node_type =="rER" and has_rER):
                G.add_node(node.er_id, label = node.er_title, title=node.er_alternative, shape="triangle" , color= self.all_colors.rER_node_color, url = str(node.er_url))
            elif(node_type =="iER" and has_iER):
                # G.add_node(node.er_id, label = node.er_title, title=node.er_alternative, shape="circle" , color= self.all_colors.iER_node_color, url = str(node.er_url))
                G.add_node(node.er_id, label = node.er_title, title=node.er_alternative, shape="circle" , color= self.all_colors.iER_node_color,x = position, y=0, fixed = True, url = str(node.er_url))
                position = position + 450
            elif(has_atomicER):
                toolTip = Views.__get_tool_tip(self, node)
                G.add_node(node.er_id, label = node.er_title, title=toolTip , color= self.all_colors.atomic_node_color, isPartOf=node.er_isPartOf, url = str(node.er_url))
    
    def __create_assesses_relationship(self, G):
        for node in self.nodeList:
            assess_id = Views.__get_node_int_id(node.er_assesses)
            if(type(assess_id) == int):
                node_being_assessed = Views.__Find_node(self,assess_id)
                G.add_edge(node.er_id, node_being_assessed.er_id, color= self.all_colors.assess_relationship_color)

    def __Find_node(self,assess_id):
        node = self.nodeList[assess_id]
        return node
    
    def __create_comesAfter_relationship_SA(self, G):
        for node in self.nodeList:
            comesAfter_id = Views.__get_node_int_id(node.er_comesAfter)
            if(type(comesAfter_id) == int):
                last_node = Views.__Find_node(self,comesAfter_id)
                current_type = node.er_type
                if( current_type=="aER" or current_type=="end"):
                    limit = len(self.nodeList)
                    while(last_node.er_type == "iER" and limit <= 0):
                        print("y")
                        last_node_comesAfter = Views.__get_node_int_id(last_node.er_comesAfter)
                        if(type(last_node_comesAfter)==int):
                            last_node = Views.__Find_node(self,last_node_comesAfter)
                        limit = limit -1
                    G.add_edge(last_node.er_id,node.er_id, weight = 5, color= self.all_colors.comesAfter_relationship_color)


    def __create_comesAfter_relationship(self, G):
        for node in self.nodeList:
            comesAfter_id = Views.__get_node_int_id(node.er_comesAfter)
            if(type(comesAfter_id) == int):
                last_node = Views.__Find_node(self,comesAfter_id)
                G.add_edge(last_node.er_id, node.er_id, weight = 5, color= self.all_colors.comesAfter_relationship_color)
    
    def __create_requires_relationshipAll(self, G, is_composite_relationship):
        for node in self.nodeList:
            require_id_list = []
            comesAfter_id = Views.__get_node_int_id(node.er_comesAfter)
            isPartOf_id = Views.__get_node_int_id(node.er_isPartOf)
            nodeA = node.er_id
            require_ids = node.er_requires

            if(type(require_ids) == str and require_ids !=""):
                require_id_list = require_ids.split(",")
            
            if(len(require_id_list) != 0 ):
                for i in range(len(require_id_list)):
                    r = Views.__get_node_int_id(require_id_list[i])
                    required_node =  Views.__Find_node(self,r)
                    nodeB = required_node.er_id
                    if(r == comesAfter_id):
                        G.remove_edge(comesAfter_id, node.er_id )
                        G.add_edge(nodeB, nodeA, weight = 5, color= self.all_colors.requires_node_color)
                    elif (r != comesAfter_id and(type(isPartOf_id) != str and is_composite_relationship)):
                        container_node = Views.__Find_node(self,isPartOf_id)
                        required_node_isPartOf =   Views.__get_node_int_id(required_node.er_isPartOf) 
                        required_node_container = Views.__Find_node(self, required_node_isPartOf )
                        if(container_node.er_id != required_node_container.er_id):
                            nodeA =  container_node.er_id
                            nodeB = required_node_container.er_id
                            G.add_edge(nodeB, nodeA, weight = 5, color= self.all_colors.requires_node_color)
                    

    def __create_isPartOf_relationship(self, G):
        for node in self.nodeList: 
            isPartOf_id = Views.__get_node_int_id(node.er_isPartOf)
            if(type(isPartOf_id) == int):
                container_node = Views.__Find_node(self,isPartOf_id)
                G.add_edge(container_node.er_id, node.er_id, color= self.all_colors.isPartOf_relationship_color)
    
    def __get_node_int_id(node):
        try: 
            node_id_int = int(node)
        except:
             node_id_int = ""
        return  node_id_int
        
    def __get_tool_tip(self, node):
        text = ""
        try: 
            isPartOf_id = int(node.er_isPartOf)
        except:
            isPartOf_id = ""
        if(type(isPartOf_id)!=str): 
          container_node = Views.__Find_node(self,isPartOf_id)
          container_node_type = container_node.er_type
          if(container_node_type == "iER"):
              text = text + "Instructional ER \n\n"
              # type of the atomic ER e.g. ebook, video,...
              er_type = node.er_type
              text += "Type:"+er_type+"\n"
              # name of the atomic ER
              text += "Name: " + node.er_title + "\n"
          elif(container_node_type == "aER"):
              text = text + "Activity ER \n\n"
              text += "Name: " + node.er_title + "\n"
              assumes = "NA\n"
              text+="Assumes: " + assumes
          elif(container_node_type == "rER"):
              try: 
                  assess_id = int(container_node.er_assesses)
              except:
                  assess_id = ""
              text = text + "Rubric ER\n\n"  
              er_assesses = ""
              if(type(assess_id)!=str):
                  er_assesses = Views.__Find_node(self,assess_id).er_id
              text += "Assessment of aER" + str(er_assesses) + "\n"
              grade = "NA \n"
              text += "Grades: " + grade
          text += "Available link: "
          if(type(node.er_url) == str):
              text += str(node.er_url) +"\n"
          else:
              text += "NA \n"  
          # adding unique id 
          unique_id = container_node_type + str(node.er_id)
          text += "ID: "+ unique_id

        return text
    
    def __get_position(self):
        count = 0
        for node in self.nodeList:
            if(node.er_type == "aER" or node.er_type == "iER"):
                count = count + 1
        num_edges = count + 1
        # each edge has a lenght of 450
        required_space = num_edges * 540
        init_position = -(required_space/2)
        return init_position