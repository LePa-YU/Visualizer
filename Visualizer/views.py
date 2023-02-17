from csv import reader
import networkx as nx
import pyvisToHtml
import nxToPyvis
import node
import colors
import math


class Views:
    def __init__(self, dataCSV):
        self.data = dataCSV.to_records(index=False).tolist()
        self.nodeList=[]
        for er in self.data:
            er_node = node.Node(er)
            self.nodeList.append(er_node)

    
    def Summative_assessment_only(self, bg, font_color, file_label, view):
        # create networkx graph
        G = nx.DiGraph()
        #aER = true, rER = true, iER = false, atomicER=false
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

    def setColors(self, aER_node_color, rER_node_color, iER_node_color,  general_node_color, assess_edge_color, requires_edge_color, isPartOf_edge_color, start_node, end_node):
        self.all_colors = colors.Color(aER_node_color, rER_node_color, iER_node_color,  general_node_color, assess_edge_color, requires_edge_color, isPartOf_edge_color, start_node, end_node)

    def getColors(self):
        return self.all_colors

    def __addNodes(self, G, has_aER, has_rER, has_iER, has_atomicER):
        for node in self.nodeList:
            node_type = node.er_type
            if(node_type == "start"):
                G.add_node(node.er_id, label = node.er_title, title=node.er_alternative, shape="diamond", color= self.all_colors.start_node_color,size=20, x = -1000, y=0, fixed = True, url = str(node.er_url))
            elif(node_type == "end"):
                G.add_node(node.er_id, label = node.er_title, title=node.er_alternative, shape="diamond", color= self.all_colors.end_node_color,size=20, x = 1000, y=0, fixed = True, url = str(node.er_url))
            elif(node_type =="aER" and has_aER):
                G.add_node(node.er_id, label = node.er_title, title=node.er_alternative, shape="box", color= self.all_colors.aER_node_color, url = str(node.er_url))
            elif(node_type =="rER" and has_rER):
                G.add_node(node.er_id, label = node.er_title, title=node.er_alternative, shape="triangle" , color= self.all_colors.rER_node_color, url = str(node.er_url))
            elif(node_type =="iER" and has_iER):
                G.add_node(node.er_id, label = node.er_title, title=node.er_alternative, shape="circle" , color= self.all_colors.iER_node_color, url = str(node.er_url))
            elif(has_atomicER):
                toolTip = Views.__get_tool_tip(self, node)
                G.add_node(node.er_id, label = node.er_title, title=toolTip , color= self.all_colors.atomic_node_color, isPartOf=node.er_isPartOf, url = str(node.er_url))
    
    def __create_assesses_relationship(self, G):
        for node in self.nodeList:
            try: 
                assess_id = int(node.er_assesses)
            except:
                assess_id = ""
            if(type(assess_id) == int):
                node_being_assessed = Views.__Find_node(self,assess_id)
                G.add_edge(node.er_id, node_being_assessed.er_id, color= self.all_colors.assess_relationship_color)

    def __Find_node(self,assess_id):
        node = self.nodeList[assess_id]
        return node
    
    def __create_comesAfter_relationship_SA(self, G):
        for node in self.nodeList:
            try:
                comesAfter_id = int(node.er_comesAfter)
            except:
                comesAfter_id = ""
            if(type(comesAfter_id) == int):
                last_node = Views.__Find_node(self,comesAfter_id)
                current_type = node.er_type
                if( current_type=="aER" or current_type=="end"):
                    while(last_node.er_type == "iER"):
                        try:
                            last_node_comesAfter = int(last_node.er_comesAfter)
                        except:
                            last_node_comesAfter = ""
                        if(type(last_node_comesAfter)==int):
                            last_node = Views.__Find_node(self,last_node_comesAfter)
                    G.add_edge(last_node.er_id,node.er_id, weight = 5, color= self.all_colors.comesAfter_relationship_color)


    def __create_comesAfter_relationship(self, G):
        for node in self.nodeList:
            try: 
                comesAfter_id = int(node.er_comesAfter)
            except:
                comesAfter_id = ""
            if(type(comesAfter_id) == int):
                last_node = Views.__Find_node(self,comesAfter_id)
                G.add_edge(last_node.er_id, node.er_id, weight = 5, color= self.all_colors.comesAfter_relationship_color)

    def __create_isPartOf_relationship(self, G):
        for node in self.nodeList:
            try: 
                isPartOf_id = int(node.er_isPartOf)
            except:
                isPartOf_id = ""
            if(type(isPartOf_id) == int):
                container_node = Views.__Find_node(self,isPartOf_id)
                G.add_edge(container_node.er_id, node.er_id, color= self.all_colors.isPartOf_relationship_color)
    
    def __get_tool_tip(self, node):
        text = ""
        try: 
            isPartOf_id = int(node.er_isPartOf)
        except:
            isPartOf_id = ""
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