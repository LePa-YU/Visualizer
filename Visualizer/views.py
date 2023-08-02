from csv import reader
import networkx as nx
import pyvisToHtml
import nxToPyvis
import node
import colors
import csv


class Views:
    spacing = 400
    def __init__(self, dataCSV, csvRows):
        # all the data headers are in lower case to ensure consistent connection in Node class
        dataCSV.columns = dataCSV.columns.str.lower()
        self.data = dataCSV.to_dict('records')

        self.nodeList=[]
        for er in self.data:
            er_node = node.Node(er)
            self.nodeList.append(er_node)

        self.csvRows = csvRows

    def set_select_edit_node(self, node_id, node2_id):
        self.select_edit_node_id = node_id
        self.select_edit_node2_id =node2_id
    def Summative_assessment_only(self, bg, font_color, file_label, view, physics, d_btn):
        # create networkx graph
        G = nx.DiGraph()
        # aER = true, rER = true, iER = false, atomicER=false, isFixed
        Views.__addNodes(self, G, True, True, False, False, False, False, True, False)
        Views.__create_assesses_relationship(self, G)
        Views. __create_comesAfter_relationship_SA(self, G)
        # assign a file name
        file_name = file_label+"_Summative_assessment_only.html"
        #convert the network to pyvis
        nxToPyvis.convert_to_pyvis(G, file_name, bg, font_color ,file_label, view, physics, True, d_btn, self.csvRows, False, self.select_edit_node_id, self.select_edit_node2_id)
    
    def Course_Overview(self, bg,font_color, file_label, view, physics, d_btn):
        # create networkx graph
        G = nx.DiGraph()
        #aER = true, rER = true, iER = false, atomicER=false, isFixed
        Views.__addNodes(self, G, True, True, True, False, False, False, True, False)
        Views.__create_assesses_relationship(self, G)
        Views. __create_comesAfter_relationship(self, G)
        # assign a file name
        file_name = file_label+"_Course_Overview.html"
        #convert the network to pyvis
        nxToPyvis.convert_to_pyvis(G, file_name, bg, font_color ,file_label, view, physics, True, d_btn, self.csvRows, False, self.select_edit_node_id, self.select_edit_node2_id)

    def  All_ERs(self, bg,font_color, file_label, view, physics, d_btn):
        # create networkx graph
        G = nx.DiGraph()
        #aER = true, rER = true, iER = true, atomicER=true, isFixed
        Views.__addNodes(self, G, True, True, True, True, False, True, True, False)
        Views.__create_assesses_relationship(self, G)
        Views. __create_comesAfter_relationship(self, G)
        Views. __create_isPartOf_relationship(self, G)
        # assign a file name
        file_name = file_label+"_All_ERs.html"
        #convert the network to pyvis
        nxToPyvis.convert_to_pyvis(G, file_name, bg, font_color ,file_label, view, physics, True, d_btn, self.csvRows, False, self.select_edit_node_id, self.select_edit_node2_id)
    
    def Requirements(self, bg,font_color, file_label, view, physics, d_btn):
         # create networkx graph
        G = nx.DiGraph()
        #has_aER, has_rER, has_iER, has_atomicER, isFixed, colorOnly, isHorizontal
        Views.__addNodes(self, G, True, True, True, True, False, False, True, True)
        Views.__create_assesses_relationship(self, G)
        Views. __create_comesAfter_relationship(self, G)
        Views. __create_isPartOf_relationship(self, G)
        Views.__create_requires_relationshipAll(self, G)
        # assign a file name
        file_name = file_label+"_requirements.html"
        # check if nodes have coordinates
        all_has_coordinate = True
        for node in self.nodeList:
            if (type(node.er_x_value) != int or type(node.er_y_value)!=int):
                all_has_coordinate = False
                break
        #convert the network to pyvis
        nxToPyvis.convert_to_pyvis(G, file_name, bg, font_color ,file_label, view, physics, True, d_btn, self.csvRows, all_has_coordinate, self.select_edit_node_id, self.select_edit_node2_id)
    
    def vertical_Requirements(self, bg,font_color, file_label, view, physics, d_btn):
         # create networkx graph
        G = nx.DiGraph()
        #has_aER, has_rER, has_iER, has_atomicER, isFixed, colorOnly, isHorizontal
        Views.__addNodes(self, G, True, True, True, True, False, False, False, False)
        Views.__create_assesses_relationship(self, G)
        Views. __create_comesAfter_relationship(self, G)
        Views. __create_isPartOf_relationship(self, G)
        Views.__create_requires_relationshipAll(self, G)
        # assign a file name
        file_name = file_label+"_vertical_requirements.html"
        #convert the network to pyvis
        nxToPyvis.convert_to_pyvis(G, file_name, bg, font_color ,file_label, view, physics, False, d_btn, self.csvRows, False, self.select_edit_node_id, self.select_edit_node2_id)

    def set_atomic_size_limit(self, atomic_max_size, atomic_min_size, start_end_size, ier_size, aer_size, rer_size):
        self.atomic_max_size = atomic_max_size
        self.atomic_min_size = atomic_min_size
        self.start_end_size = start_end_size
        self.ier_size = ier_size
        self.aer_size = aer_size
        self.rer_size = rer_size
    
    def setColors(self, aER_node_color, rER_node_color, iER_node_color,  general_node_color, assess_edge_color, requires_edge_color, isPartOf_edge_color, start_node, end_node, requires_node, aImg, aMov, aSW, aAudio, aText, aDataset):
        self.all_colors = colors.Color(aER_node_color, rER_node_color, iER_node_color,  general_node_color, assess_edge_color, requires_edge_color, isPartOf_edge_color, start_node, end_node, requires_node, aImg, aMov, aSW, aAudio, aText, aDataset)

    def getColors(self):
        return self.all_colors

    def __addNodes(self, G, has_aER, has_rER, has_iER, has_atomicER, isFixed, colorOnly, isHorizontal, is_requirement_view):
        start_position= Views.__get_position_horizontal(self, has_aER, has_iER, has_atomicER)
        end_position = - start_position
        position = start_position + self.spacing
        rER_position = 50

        # start_end_node_size = 20
        # iER_size = 25
        # aER_size = 25
        # rER_size = 25
        start_end_node_size = self.start_end_size
        iER_size = self.ier_size
        aER_size = self.aer_size
        rER_size = self.rer_size

        # check if all nodes have x and y position
        all_has_coordinate = False
        if(is_requirement_view):
            all_has_coordinate = True
            for node in self.nodeList:
                if (type(node.er_x_value) != int or type(node.er_y_value)!=int):
                    all_has_coordinate = False
                    break
        
  
        for node in self.nodeList:
            node_type = node.er_type
            if(node_type == "start"):
                if(all_has_coordinate):
                    G.add_node(node.er_id, label = node.er_title, title=node.er_type, shape="diamond", color= self.all_colors.start_node_color,size=start_end_node_size, x = node.er_x_value, y=node.er_y_value, fixed = True, url = str(node.er_url))
                else:
                    if(isHorizontal):
                        G.add_node(node.er_id, label = node.er_title, title=node.er_type, shape="diamond", color= self.all_colors.start_node_color,size=start_end_node_size, x = start_position, y=0, fixed = True, url = str(node.er_url))
                    else:
                        G.add_node(node.er_id, label = node.er_title, title=node.er_type, shape="diamond", color= self.all_colors.start_node_color,size=start_end_node_size, x =0, y=start_position, fixed = True, url = str(node.er_url))
            elif(node_type == "end"):
                if(all_has_coordinate):
                     G.add_node(node.er_id, label = node.er_title, title=node.er_type, shape="diamond", color= self.all_colors.end_node_color,size=start_end_node_size, x = node.er_x_value, y=node.er_y_value, fixed = True, url = str(node.er_url))
                else:
                    if(isHorizontal):
                        G.add_node(node.er_id, label = node.er_title, title=node.er_type, shape="diamond", color= self.all_colors.end_node_color,size=start_end_node_size, x = end_position, y=0, fixed = True, url = str(node.er_url))
                    else:
                        G.add_node(node.er_id, label = node.er_title, title=node.er_type, shape="diamond", color= self.all_colors.end_node_color,size=start_end_node_size, x = 0, y=end_position, fixed = True, url = str(node.er_url))
            elif(node_type =="aER" and has_aER):
                if(all_has_coordinate):
                    G.add_node(node.er_id, label = node.er_title, title=node.er_type, shape="box", value = 1, scaling = Views.__get_atomic_node_scaling_property(aER_size), color= self.all_colors.aER_node_color,x = node.er_x_value, y=node.er_y_value, url = str(node.er_url))
                else:
                    if(isFixed):
                        G.add_node(node.er_id, label = node.er_title, title=node.er_type, shape="box", color= self.all_colors.aER_node_color,x = position, y=0, url = str(node.er_url))
                        position = position+self.spacing
                    else:
                        G.add_node(node.er_id, label = node.er_title, title=node.er_type, shape="box",value = 1, scaling = Views.__get_atomic_node_scaling_property(aER_size) , color= self.all_colors.aER_node_color, url = str(node.er_url))
            elif(node_type =="rER" and has_rER):
                if(all_has_coordinate):
                    G.add_node(node.er_id, label = node.er_title, title=node.er_type, shape="triangle" , size =rER_size,color= self.all_colors.rER_node_color, x = node.er_x_value, y = node.er_y_value, url = str(node.er_url))
                else:
                    G.add_node(node.er_id, label = node.er_title, title=node.er_type, shape="triangle" , size = rER_size ,color= self.all_colors.rER_node_color, url = str(node.er_url))
            elif(node_type =="iER" and has_iER):
                if(all_has_coordinate):
                    G.add_node(node.er_id, label = node.er_title, title=node.er_type, shape="circle" ,value = 1, scaling = Views.__get_atomic_node_scaling_property(iER_size), color= self.all_colors.iER_node_color,x = node.er_x_value, y=node.er_y_value, url = str(node.er_url))
                else:
                    if(isFixed):
                        G.add_node(node.er_id, label = node.er_title, title=node.er_type, shape="circle" , color= self.all_colors.iER_node_color,x = position, y=0, fixed = True, url = str(node.er_url))
                        position = position + self.spacing
                    else:
                        G.add_node(node.er_id, label = node.er_title, title=node.er_type, shape="circle" , value = 1, scaling = Views.__get_atomic_node_scaling_property(iER_size) ,color= self.all_colors.iER_node_color, url = str(node.er_url))
            elif(node_type == "IP"):
                pass
            elif(has_atomicER and type(node_type)==str):
                toolTip = Views.__get_tool_tip(self, node)
                Views.__add_atomic_nodes(self, G, node, toolTip, colorOnly, all_has_coordinate)
    def __get_atomic_node_scaling_property(size):
        res={
            "label":{
                "enabled": True,
                "min": size,
                "max": size
            },
        }
        return res
    def __add_atomic_nodes(self, G, node, toolTip, colorOnly, all_has_coordinate):
        node_type = node.er_type
        atomic_size = Views.__get_atomic_size_size(self,node)
        
        if(colorOnly):
            #all_er view:
            if(node_type == ".png" or node_type ==".jpeg"):
                G.add_node(node.er_id, label = node.er_title, title=toolTip , color= self.all_colors.atomic_node_color_img, isPartOf=node.er_isPartOf, url = str(node.er_url))
            elif(node_type == ".mov" or node_type ==".mp4"):
                G.add_node(node.er_id, label = node.er_title, title=toolTip , color= self.all_colors.atomic_node_color_mov, isPartOf=node.er_isPartOf, url = str(node.er_url))
            elif(node_type == ".exe" or node_type ==".ipynd" or node_type ==".app"):
                G.add_node(node.er_id, label = node.er_title, title=toolTip , color= self.all_colors.atomic_node_color_software, isPartOf=node.er_isPartOf, url = str(node.er_url))
            elif(node_type == ".mp3" or node_type ==".wav"):
                G.add_node(node.er_id, label = node.er_title, title=toolTip , color= self.all_colors.atomic_node_color_audio, isPartOf=node.er_isPartOf, url = str(node.er_url))
            elif(node_type == ".txt" or node_type ==".pdf" or node_type==".html" or node_type==".md" or node_type==".pptx" or node_type==".dvi"):
                G.add_node(node.er_id, label = node.er_title, title=toolTip , color= self.all_colors.atomic_node_color_text, isPartOf=node.er_isPartOf, url = str(node.er_url))
            elif(node_type == ".csv" or node_type ==".xlsx"):
                G.add_node(node.er_id, label = node.er_title, title=toolTip , color= self.all_colors.atomic_node_color_dataset, isPartOf=node.er_isPartOf, url = str(node.er_url))
            elif(node_type==".zip"):
                G.add_node(node.er_id, label = node.er_title, title=toolTip , color= self.all_colors.atomic_node_color_coll, isPartOf=node.er_isPartOf, url = str(node.er_url))
            else:
                G.add_node(node.er_id, label = node.er_title, title=toolTip, isPartOf=node.er_isPartOf, url = str(node.er_url))
        else:
            # requirement view
            if(node_type == ".png" or node_type ==".jpeg"):
                if(all_has_coordinate):
                    G.add_node(node.er_id, label = node.er_title, title=toolTip ,shape="circularImage", image="https://raw.githubusercontent.com/LePa-YU/Visualizer/development/Visualizer/images/image.svg", color=Views.__get_atomic_node_color_property(self.all_colors.atomic_node_color_img),size = atomic_size, isPartOf=node.er_isPartOf, x = node.er_x_value, y = node.er_y_value, url = str(node.er_url))
                else:
                    G.add_node(node.er_id, label = node.er_title, title=toolTip ,shape="circularImage", image="https://raw.githubusercontent.com/LePa-YU/Visualizer/development/Visualizer/images/image.svg", color=Views.__get_atomic_node_color_property(self.all_colors.atomic_node_color_img),size = atomic_size, isPartOf=node.er_isPartOf, url = str(node.er_url))
            elif(node_type == ".mov" or node_type ==".mp4"):
                if(all_has_coordinate):
                    G.add_node(node.er_id, label = node.er_title, title=toolTip ,shape="circularImage", image="https://raw.githubusercontent.com/LePa-YU/Visualizer/development/Visualizer/images/video.svg", color=Views.__get_atomic_node_color_property(self.all_colors.atomic_node_color_mov),size = atomic_size,isPartOf=node.er_isPartOf, x = node.er_x_value, y = node.er_y_value, url = str(node.er_url))
                else:
                    G.add_node(node.er_id, label = node.er_title, title=toolTip ,shape="circularImage", image="https://raw.githubusercontent.com/LePa-YU/Visualizer/development/Visualizer/images/video.svg", color=Views.__get_atomic_node_color_property(self.all_colors.atomic_node_color_mov),size = atomic_size,isPartOf=node.er_isPartOf, url = str(node.er_url))
            elif(node_type == ".exe" or node_type ==".ipynd" or node_type ==".app"):
                if(all_has_coordinate):
                    G.add_node(node.er_id, label = node.er_title, title=toolTip , shape="circularImage", image="https://raw.githubusercontent.com/LePa-YU/Visualizer/development/Visualizer/images/software.svg", color=Views.__get_atomic_node_color_property(self.all_colors.atomic_node_color_software),size = atomic_size,isPartOf=node.er_isPartOf, x = node.er_x_value, y = node.er_y_value, url = str(node.er_url))
                else:
                    G.add_node(node.er_id, label = node.er_title, title=toolTip , shape="circularImage", image="https://raw.githubusercontent.com/LePa-YU/Visualizer/development/Visualizer/images/software.svg", color=Views.__get_atomic_node_color_property(self.all_colors.atomic_node_color_software),size = atomic_size,isPartOf=node.er_isPartOf, url = str(node.er_url))
            elif(node_type == ".mp3" or node_type ==".wav"):
                if(all_has_coordinate):
                    G.add_node(node.er_id, label = node.er_title, title=toolTip , shape="circularImage", image="https://raw.githubusercontent.com/LePa-YU/Visualizer/development/Visualizer/images/audio.svg", color=Views.__get_atomic_node_color_property(self.all_colors.atomic_node_color_audio),size = atomic_size,isPartOf=node.er_isPartOf, x = node.er_x_value, y = node.er_y_value, url = str(node.er_url))
                else:
                    G.add_node(node.er_id, label = node.er_title, title=toolTip , shape="circularImage", image="https://raw.githubusercontent.com/LePa-YU/Visualizer/development/Visualizer/images/audio.svg", color=Views.__get_atomic_node_color_property(self.all_colors.atomic_node_color_audio),size = atomic_size,isPartOf=node.er_isPartOf, url = str(node.er_url))
            elif(node_type == ".txt" or node_type ==".pdf" or node_type==".html" or node_type==".md" or node_type==".pptx" or node_type==".dvi"):
                if(all_has_coordinate):
                    G.add_node(node.er_id, label = node.er_title, title=toolTip , shape="circularImage", image = "https://raw.githubusercontent.com/LePa-YU/Visualizer/development/Visualizer/images/text.svg", color=Views.__get_atomic_node_color_property(self.all_colors.atomic_node_color_text),size = atomic_size, isPartOf=node.er_isPartOf, x = node.er_x_value, y = node.er_y_value, url = str(node.er_url))
                else:
                    G.add_node(node.er_id, label = node.er_title, title=toolTip , shape="circularImage", image = "https://raw.githubusercontent.com/LePa-YU/Visualizer/development/Visualizer/images/text.svg", color=Views.__get_atomic_node_color_property(self.all_colors.atomic_node_color_text),size = atomic_size, isPartOf=node.er_isPartOf, url = str(node.er_url))
            elif(node_type == ".csv" or node_type ==".xlsx"):
                if(all_has_coordinate):
                    G.add_node(node.er_id, label = node.er_title, title=toolTip , shape="circularImage", image="https://raw.githubusercontent.com/LePa-YU/Visualizer/development/Visualizer/images/data.svg", color=Views.__get_atomic_node_color_property(self.all_colors.atomic_node_color_dataset),size = atomic_size,isPartOf=node.er_isPartOf,  x = node.er_x_value, y = node.er_y_value, url = str(node.er_url))
                else:
                    G.add_node(node.er_id, label = node.er_title, title=toolTip , shape="circularImage", image="https://raw.githubusercontent.com/LePa-YU/Visualizer/development/Visualizer/images/data.svg", color=Views.__get_atomic_node_color_property(self.all_colors.atomic_node_color_dataset),size = atomic_size,isPartOf=node.er_isPartOf, url = str(node.er_url))
            elif(node_type==".zip"):
                if(all_has_coordinate):
                     G.add_node(node.er_id, label = node.er_title, title=toolTip , shape="circularImage", image="https://raw.githubusercontent.com/LePa-YU/Visualizer/development/Visualizer/images/zip.svg", color=Views.__get_atomic_node_color_property(self.all_colors.atomic_node_color_coll),size = atomic_size,isPartOf=node.er_isPartOf,  x = node.er_x_value, y = node.er_y_value, url = str(node.er_url))
                else:
                    G.add_node(node.er_id, label = node.er_title, title=toolTip , shape="circularImage", image="https://raw.githubusercontent.com/LePa-YU/Visualizer/development/Visualizer/images/zip.svg", color=Views.__get_atomic_node_color_property(self.all_colors.atomic_node_color_coll),size = atomic_size,isPartOf=node.er_isPartOf, url = str(node.er_url))
            else:
                if(all_has_coordinate):
                     G.add_node(node.er_id, label = node.er_title, title=toolTip, isPartOf=node.er_isPartOf, x = node.er_x_value, y = node.er_y_value, url = str(node.er_url))
                else:
                    G.add_node(node.er_id, label = node.er_title, title=toolTip, isPartOf=node.er_isPartOf, url = str(node.er_url))
    
    def __get_atomic_size_size(self,node):
        size = 0
        atomic_min_allowed = self.atomic_min_size
        atomic_max_allowed = self.atomic_max_size
        #ration for increment
        atomic_increments = Views.__get_atomic_size_increment(self, atomic_min_allowed, atomic_max_allowed)

        atomic_dur = Views.__get_node_int_id(node.er_duration)
        if(type(atomic_dur)!= int):
            atomic_dur = 0
        #update size
        # print(atomic_increments)
        size = atomic_min_allowed + (atomic_increments * (atomic_dur))
        return size

    def __get_atomic_size_increment(self, min_size, max_size):
        increment = 0

        allowed_diff = (max_size - min_size)

        max_dur = max(self.nodeList, key=lambda d: d.er_duration).er_duration
        min_dur = Views.__get_second_Min_duration(self) # min is always 0
        dur_diff = max_dur - min_dur
        if(dur_diff == 0):
            increment = 0
        else:
            increment = allowed_diff/dur_diff

        return increment

    def __get_second_Min_duration(self):
        min = 0
        copy_list = self.nodeList.copy()
        copy_list.sort(key=lambda x: x.er_duration)
        for n in copy_list:
            if (n.er_duration != 0):
                min = n.er_duration
                break; 
        return min
        
    def __get_atomic_node_color_property(color):
        res={
            "border":"white", 
            "background":"white",
            "highlight":{
                "border":color,
                "background": color
            },
            "hover":{
                "border": color ,
                "background": color
            },
        }
        return res
    def __create_assesses_relationship(self, G):
        for node in self.nodeList:
            assess_id = Views.__get_node_int_id(node.er_assesses)
            if(type(assess_id) == int):
                node_being_assessed = Views.__Find_node(self,assess_id)
                G.add_edge(node.er_id, node_being_assessed.er_id, color= self.all_colors.assess_relationship_color)

    def __Find_node(self,n_id):
        # node = self.nodeList[assess_id]
        node = None
        for n in self.nodeList:
            if n.er_id == n_id:
                node = n
                break
            # print(n.er_id)
        return node
    
    def __create_comesAfter_relationship_SA(self, G):
        for node in self.nodeList:
            comesAfter_id = Views.__get_node_int_id(node.er_comesAfter)
            if(type(comesAfter_id) == int):
                last_node = Views.__Find_node(self,comesAfter_id)
                current_type = node.er_type
                if( current_type=="aER" or current_type=="end"):
                    limit = len(self.nodeList)
                    if last_node!=None:
                        while(last_node.er_type == "iER"):
                            last_node_comesAfter = Views.__get_node_int_id(last_node.er_comesAfter)
                            if(type(last_node_comesAfter)==int):
                                last_node = Views.__Find_node(self,last_node_comesAfter)
                            else:
                                break  
                        G.add_edge(last_node.er_id,node.er_id, weight = 5, color= self.all_colors.comesAfter_relationship_color)


    def __create_comesAfter_relationship(self, G):
        for node in self.nodeList:
            comesAfter_id = Views.__get_node_int_id(node.er_comesAfter)
            if(type(comesAfter_id) == int):
                last_node = Views.__Find_node(self,comesAfter_id)
                if last_node != None:
                    G.add_edge(last_node.er_id, node.er_id, weight = 5, color= self.all_colors.comesAfter_relationship_color)
    
    def __create_requires_relationshipAll(self, G):
        for node in self.nodeList:
            require_id_list = []
            comesAfter_id = Views.__get_node_int_id(node.er_comesAfter)
            isPartOf_id = Views.__get_node_int_id(node.er_isPartOf)
            current_node_id = node.er_id
            current_node_type = node.er_type
            current_is_Atomic = Views.__isAtomic(current_node_type)
            require_ids = node.er_requires
            if(type(require_ids) == str and require_ids!=""):
                require_id_list = require_ids.split(",")
            else:
                try:
                    require_ids = int(require_ids)
                except:
                    require_ids = ""
                
                if(type(require_ids)==int):
                    require_id_list.append(require_ids)
            # print(require_id_list)
            # if(len(require_id_list) != 0 ):
            for i in range(len(require_id_list)):
                r = Views.__get_node_int_id(require_id_list[i])
                # print(r)
                required_node =  Views.__Find_node(self,r)
                required_node_id = None; required_node_type = None
                if required_node != None:
                    required_node_id = required_node.er_id
                    required_node_type = required_node.er_type
                required_is_Atomic = Views.__isAtomic(required_node_type)
                    # G.add_edge(required_node_id, current_node_id , weight = 5, color= self.all_colors.requires_node_color)
                if((required_node_id!=None and current_node_id!=None)and (required_node_id == comesAfter_id)): # if the there is both comesAfter and requires between two nodes
                        # G.remove_edge(comesAfter_id, node.er_id )
                    G.add_edge(required_node_id, current_node_id, weight = 5, color= self.all_colors.requires_node_color)
                elif(required_is_Atomic and current_is_Atomic):
                    current_container = Views.__get_container_Node(self, node)
                    current_container_id = None; current_container_comesAfter = None
                    if current_container != None:
                        current_container_id = current_container.er_id
                        current_container_comesAfter = current_container.er_comesAfter
                    required_container = None
                    if required_node != None:
                        required_container = Views.__get_container_Node(self, required_node)
                    required_container_id = None
                    if required_container != None:
                        required_container_id = required_container.er_id
                    # print(current_container_type + " " +required_container_type)
                    if(current_container_id != required_container_id and required_container_id != current_container_comesAfter):
                        num_nodes_in_between = Views.__get_num_of_Node_in_between(self, current_container, required_container)
                        if required_container_id != None and current_container_id != None:
                            G.add_edge(required_container_id, current_container_id, weight = 5, color= self.all_colors.requires_node_color, length=self.spacing*num_nodes_in_between*2)

    def __create_isPartOf_relationship(self, G):
        for node in self.nodeList: 
            isPartOf_id = Views.__get_node_int_id(node.er_isPartOf)
            if(type(isPartOf_id) == int):
                container_node = Views.__Find_node(self,isPartOf_id)
                if container_node != None:
                    G.add_edge(container_node.er_id, node.er_id, color= self.all_colors.isPartOf_relationship_color)
    
    def __get_num_of_Node_in_between(self, nodeA, nodeB):
        res = -1
        current_node = nodeA
        final_node= nodeB
        while((current_node!= None and final_node!= None)and(current_node.er_id != final_node.er_id)):
            res = res + 1
            current_node_comesAfter = Views.__get_node_int_id( current_node.er_comesAfter)
            current_node = Views.__Find_node(self, current_node_comesAfter)

            
        return res


    def __get_container_Node(self, node):
        current_isPartOf = Views.__get_node_int_id(node.er_isPartOf)
        container = None
        for i in range(len(self.nodeList)):
            n_id = self.nodeList[i].er_id
            if n_id == current_isPartOf: 
                container = self.nodeList[i]
        return container
    def __isAtomic(node_type):
        return node_type!="aER" and node_type!="iER" and node_type!="rER" and node_type!="start" and node_type!="end"

    def __get_node_int_id(node):
        try: node_id_int = int(node)
        except:
             try: node_id_int = int(float(node))
             except: node_id_int  = None
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
          text += "ID: "+ unique_id + "\n"

          text += "Duration: " + str(node.er_duration) + " min"

        return text
    
    def __get_position_horizontal(self, has_aER, has_iER, has_atomic):
        count = 0
        if(has_aER==True and has_iER==False):
            for node in self.nodeList:
                if(node.er_type == "aER"):
                    count = count + 1

        elif(has_aER==True and has_iER==True):
            for node in self.nodeList:
                if(node.er_type == "aER" or node.er_type == "iER"):
                    count = count + 1
        num_edges = count + 1
        # each edge has a lenght of 450
        required_space = num_edges * self.spacing
        if(has_atomic):
            required_space = required_space * 1.5
        init_position = -(required_space/2)
        return init_position