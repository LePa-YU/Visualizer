import os
import streamlit as st
import pandas as pd
import numpy as np
import time

class datasetCreator:
    def __init__(self, file_name):
        self.file_name = file_name
        if(not os.path.isfile(file_name)): 
            self.df = pd.DataFrame(columns=['identifier','title','description','url','type','isPartOf','assesses','comesAfter','requires','alternativeContent','references','isFormatOf','duration'])
            # add start and end node
            if(len(self.df.index)==0):
                self.df.loc[len(self.df.index)] = [0,'Start','start','','start','','','','','','','','']
                self.df.loc[len(self.df.index)] = [len(self.df.index),'End','end','','end','','',len(self.df.index)-1,'','','','','']
                self.df.to_csv(file_name, index=False)
        else:
            self.df = pd.read_csv(file_name)
   
    def add_node(self):
        datasetCreator.set_selected_node(self, None)
        node = datasetCreator.__create_node_addition_fields(self)
        if(node):
            end_node_comesAfter = self.df["comesAfter"].iloc[-1]
            # print(end_node_comesAfter)
            self.df.loc[len(self.df.index)-1] = node
            # print(node[0])
            self.df.loc[len(self.df.index)] = [node[0]+1,'End','end','','end','','',end_node_comesAfter,'','','','','']
            self.df.to_csv(self.file_name, index=False)
        
        
    
    def edit_node(self):
        datasetCreator.set_selected_node(self, None)
        if(len(self.df.index) <= 2):
            st.text("Dataset is empty please add a node")
        else:
            st.divider()
            st.text("find the node you want to edit:")
            node = datasetCreator.__find_node_list(self)
            # print(node)
            if(node != None):
                node = np.int16(node).item()
            datasetCreator.set_selected_node(self, node)
            disable = False
            if("delete_node" in st.session_state):
                if(st.session_state.delete_node == True): disable = True
            confirm_edit = st.checkbox("Confirm selection", key="confirm_edit")
            if(confirm_edit):
                st.divider()
                edited_node = datasetCreator.__edit_option(self, node)
                if(edited_node):
                    save_col, delete_col=st.columns([1, 3.5])
                    with save_col:
                        save_node = st.button("Save Changes", key="save_change_btn", disabled=disable)
                        if(save_node):
                            for i in range(len(self.df.index)):
                                n_id = self.df["identifier"][i]
                                if n_id == node:
                                    self.df.loc[i] = edited_node
                                    self.df.to_csv(self.file_name, index=False)
                                    break
                    with delete_col:
                        delete_node = st.button("Delete Node", key="delete_node", disabled=disable)
                        if(delete_node):
                            # print(node)
                            index = 0
                            # find the index to be removed
                            for i in range(len(self.df.index)):
                                n_id = self.df["identifier"][i]
                                if(n_id == node ):
                                    index = i
                                    break
                            # before deleting, get this node's ca, find  the node that comes after this and set it ca to this node's ca
                            for i in range(len(self.df.index)):
                                this_id = self.df["identifier"][i]
                                if(this_id == node):
                                    try: this_ca = int(self.df["comesAfter"][i])
                                    except: this_ca =None
                                    for j in range(len(self.df.index)):
                                            try: ca = int(self.df["comesAfter"][j])
                                            except: ca =None
                                            if(ca == node and ca != None):
                                                self.df["comesAfter"][j] = this_ca
                                    break
                            # if a node is referred in isPartOf another node, clear the 2nd node's isPart
                            for j in range(len(self.df.index)):
                                try: ipo = int(self.df["isPartOf"][j])
                                except: ipo = None
                                if(ipo == node and ipo != None):
                                    self.df["isPartOf"][j] = ""

                            # if a node is referred in assesses of another node, clear the 2nd node's assesses
                            for j in range(len(self.df.index)):
                                try: isb = int(self.df["assesses"][j])
                                except: isb = None
                                if(isb == node and isb != None):
                                    self.df["assesses"][j] = ""
                            
                            # if node has requires already, allow deleting the relation from node 1's requires field if node 2 is part of it
                            for i in range(len(self.df.index)):
                                require_ids = self.df["requires"][i]
                                require_id_list = []
                                if type(require_ids) != str: require_ids = str(require_ids)
                                if type(require_ids) == str and require_ids!="":
                                    require_id_list = require_ids.split(",") # convert node's requires to list
                                    for n in require_id_list: 
                                        try: n_int = int(n)
                                        except: 
                                            try: n_int = int(float(n))
                                            except: n_int = None
                                        if n_int == node :  # node exist in required field of this node 
                                            require_id_list.remove(str(n))
                                            delimiter = ','
                                            res = delimiter.join(require_id_list)
                                            self.df["requires"][i] = res
                                            
                            self.df = self.df.drop(index) # remove the node itself
                            self.df.to_csv(self.file_name, index=False)
                            self.df = pd.read_csv(self.file_name)
                     
    def add_relation(self):
        # datasetCreator.set_selected_node(self, None)
        node_with_relation = datasetCreator.__add_relation_fields(self)
        
    
    def __add_relation_fields(self):
        # datasetCreator.set_selected_node(self, None)
        col1, col2, col3 = st.columns(3)
        node1_id = None; node2_id = None
        node1_confirm = False; node2_confirm = False
        node1_is_composite = False; node1_type =""; relation_select=""
        with col1: 
            st.text("select node 1")
            node1_id = datasetCreator.__find_node1_for_relations(self)
            if(node1_id != None):
                node1_id = np.int16(node1_id).item()
            datasetCreator.set_selected_node(self, node1_id)
            node1_confirm = True 
            if(node1_confirm):
                # datasetCreator.set_selected_node(self, None)
                for i in range(len(self.df.index)):
                    node_id = self.df["identifier"][i]
                    if (node_id == node1_id):
                        node1_type = self.df["type"][i]
                        if(node1_type == "iER" or node1_type == "aER" or node1_type=="rER"): node1_is_composite = True
                        break        
        with col2:
            st.text("select relation")
            if node1_is_composite:
                # if first node is composite we can have: 
                # composite-composite relation: 
                #   1. comesAfter, comesBefore: assumption --> between aER, rER, start and end
                #       a. node1 comesAfter nodeB (add to node A)
                #       b. node1 comesBefore node B (add to node B)
                #   2. if node1_type is rER --> assess else is assessedBy
                # composite-atomic relation: hasPart --> node 1 has node 2 (for now only atomic)
                relation_list = []
                if node1_type == "rER": relation_list = ["Has Part", "Assesses"] #done
                elif node1_type == "aER":
                    # possiblity of adding ComesBefore
                    relation_list  = ["Comes After", "Has Part", "Is Assessed By"] #done
                else: 
                    # possiblity of adding ComesBefore
                    relation_list = ["Comes After", "Has Part"] #done
            else:
                # if a node a not a composite then it is atomic ER. the only atomic-atomic relation:
                #   1. Requires if node 1 requires node 2 --> add to node 1
                #   2. is required by: if node 1 is required by node 2 --> add to node 2
                # atomic_composite relations:
                # 1. is Part of: atomic ER can be part of any composite ER --> add to node 1
                relation_list = ["Requires", "Is Required By", "Is Part Of"]
            relation_select = st.selectbox("", relation_list, key="relation select")
        with col3:
            st.text("select node 2")
            # the avaiable nodes are changed based oon in col 2
            datasetCreator.__find_node2_for_relations(self, node1_id, relation_select)
        
    def __find_node2_for_relations(self, node_1, relation):
        # type_col, title_col, id_col = st.columns(3)
        # # select type: there are 4 type: iER, aER, rER, atomic ER or all --> default = All
        if "confirm_ER_2" not in st.session_state:
                st.session_state.confirm_ER_2 = False
        # based on relation the types of nodes present change:
        if(relation == "Comes After"):
            datasetCreator.__add_relation_comesAfter(self, node_1)
        if(relation == "Has Part"):
            datasetCreator.__add_relation_HasPart(self, node_1)
        if(relation == "Is Assessed By"):
            datasetCreator.__add_relation_isAssessedBy(self, node_1)
        if( relation == "Assesses"):
            datasetCreator.__add_relation_assesses(self, node_1)
        if( relation == "Is Part Of"):
            datasetCreator.__add_relation_Is_Part_Of(self, node_1)
        if( relation == "Requires"):
            datasetCreator.__add_relation_requires(self, node_1)
        # print(relation)
    
    def __add_relation_requires(self, node_1):
        ## Both node_1 and node_2 need to be atomic
        atomic_title_list = []; node_2 = None
        for i in range(len(self.df.index)):
            node_title = self.df["title"][i]
            node_type = self.df["type"][i]
            node_id = self.df["identifier"][i]
            if(node_id != node_1):
                if(node_type != "start" and node_type != "end" and node_type != "iER" and node_type != "rER" and node_type != "aER"):
                    atomic_title_list.append(node_title)
        title_selector = st.selectbox("Select atomic ER", set(atomic_title_list), key="find_node2_ha_relation", disabled= False)
        # find type or types based on title
        title_has_duplicate = datasetCreator.__title_has_duplicate(title_selector, atomic_title_list)
        node_has_duplicate = False
        type_selector  = ""
        if title_has_duplicate: 
            type_list = []
            for i in range(len(self.df.index)):
                node_title = self.df["title"][i]
                node_type = self.df["type"][i]
                node_id = self.df["identifier"][i]
                if(node_id != node_1):  
                    if (node_title == title_selector):
                        if(node_type != "start" and node_type != "end" and node_type != "iER" and node_type != "rER" and node_type != "aER"):
                            type_list.append(node_type)
            type_selector = st.selectbox("Select ER type", set(type_list), key = "find_node2_req_type")
            node_has_duplicate = datasetCreator.__title_has_duplicate(type_selector, type_list)    
        # if the there are duplicate titles (there can be duplicate nodes --> only IDs are unique) then we need id field to find 
        # the correct node
        id_selector = ""
        if( node_has_duplicate):
            id_list = []
            for i in range(len(self.df.index)):
                node_id = self.df["identifier"][i]
                node_title = self.df["title"][i]
                node_type = self.df["type"][i]
                if(node_id != node_1):  
                    if(node_type == type_selector):
                        if(title_selector == node_title): id_list.append(node_id)
            id_selector = st.selectbox("Select ID: ", id_list, key="find_node2_id_relation", disabled= False)    
        if(id_selector): node_2 = int(id_selector)
        else:
            #if node is unique --> no id selector --> find id
            for i in range(len(self.df.index)):
                node_id = self.df["identifier"][i]
                node_title = self.df["title"][i]
                node_type = self.df["type"][i]
                if node_id != node_1:
                    if type_selector == "":
                        if title_selector == node_title: 
                            if(node_type != "start" and node_type != "end" and node_type != "iER" and node_type != "rER" and node_type != "aER"):    
                                node_2 = node_id
                    else:
                        if(node_type == type_selector and title_selector == node_title): node_2 = node_id
        if(node_2!= None):
            node_2 = np.int16(node_2).item()
        datasetCreator.set_selected_node2(self, node_2)  
        
        #Relation itself:
        # node 1 requires node 2 --> node 2 id added to node 1's requires field
        # requires field is a list so it must retrieve and add to the list
        add_relation = st.button("Add Relation", key="add_relation_ha")
        if(add_relation):
            for i in range(len(self.df.index)):
                n_id = self.df["identifier"][i]
                if(n_id == node_1): # find node 1
                    if(pd.isna(self.df["requires"][i])): # requires field is empty
                        self.df["requires"][i] =  str(int(node_2))
                    else:
                        self.df["requires"][i] = str(self.df["requires"][i]) +"," + str(int(node_2))
                    # self.df["requires"][i] =  node_2
                    break
        # if node 1 has requires already, allow deleting the relation from node 1's requires field if node 2 is part of it
        flag = False; node_1_requires = []; index = None; n2 = None
        for i in range(len(self.df.index)):
            n_id = self.df["identifier"][i]
            if(n_id == node_1): # find node 1
                require_ids = self.df["requires"][i]
                require_id_list = []
                if type(require_ids) != str: require_ids = str(require_ids)
                if type(require_ids) == str and require_ids!="":
                    require_id_list = require_ids.split(",")
                        # find node 2:
                    for n in require_id_list:
                        # print(node_2)
                        try: n_int = int(n)
                        except: 
                            try: n_int = int(float(n))
                            except: n_int = None
                        if n_int == node_2 :  # node exist in required field of node 1 
                            flag = True; node_1_requires = require_id_list.copy()
                            index = i; n2 = n
                            break
        # print(node_1_requires); print(n2)
        if flag:
            del_relation = st.button("Delete Relation", key="del_relation_r")
            if del_relation:
                # print(node_1_requires)
                # print(str(node_2))
                node_1_requires.remove(str(n2))
                delimiter = ','
                res = delimiter.join(node_1_requires)
                if index != None: self.df["requires"][index] = res
                              
        self.df.to_csv(self.file_name, index=False)

    def __add_relation_Is_Part_Of(self, node_1):
        # Is part of is only possible if node 1 is atomic and node 2 is composite
        # so the option for node are all composite --> choose type, choose title, choose ID
        type_selector = st.selectbox("Select Type:", ("All", "aER", "rER", "iER"))
        aer_list = []; ier_list = []; rer_list = []; all_list = []; node_2 = None
        for i in range(len(self.df.index)):
            node_title = self.df["title"][i]
            node_type = self.df["type"][i]
            if(node_type != "start" and node_type != "end"):
                if node_type == "aER": 
                    aer_list.append(node_title); all_list.append(node_title)
                if node_type == "iER": 
                    ier_list.append(node_title); all_list.append(node_title)
                if node_type == "rER": 
                    rer_list.append(node_title); all_list.append(node_title)
        if type_selector == "All": 
            title_selector = st.selectbox("Select ER", set(all_list))
            title_has_duplicate = datasetCreator.__title_has_duplicate(title_selector, all_list)
        elif type_selector == "aER": 
            title_selector = st.selectbox("Select ER", set(aer_list))
            title_has_duplicate = datasetCreator.__title_has_duplicate(title_selector, aer_list)
        elif type_selector == "rER": 
            title_selector = st.selectbox("Select ER", set(rer_list))
            title_has_duplicate = datasetCreator.__title_has_duplicate(title_selector, rer_list)
        elif type_selector == "iER": 
            title_selector = st.selectbox("Select ER", set(ier_list))  
            title_has_duplicate = datasetCreator.__title_has_duplicate(title_selector, ier_list)
        
        id_selector = ""
        if(title_has_duplicate):
            id_list = []
            for i in range(len(self.df.index)):
                node_id = self.df["identifier"][i]
                node_title = self.df["title"][i]
                node_type = self.df["type"][i]
                if(type_selector == "All"):
                    if (node_type == "aER" or node_type == "iER" or node_type == "rER"):
                        if(title_selector == node_title): id_list.append(node_id)
                else:
                    if(type_selector == node_type and title_selector == node_title): id_list.append(node_id)
            id_selector = st.selectbox("Select ID: ", id_list)    
        if(id_selector):
           node_2 =  int(id_selector)
        else:
            #if node is unique --> no id selector --> find id
            for i in range(len(self.df.index)):
                node_id = self.df["identifier"][i]
                node_title = self.df["title"][i]
                node_type = self.df["type"][i]
                if(type_selector == "All"):
                    if(node_type == "aER" or node_type =="iER" or node_type =="rER"):
                        if(title_selector == node_title): node_2 = node_id
                else:
                    if(type_selector == node_type and title_selector == node_title): node_2 = node_id
       
        if(node_2!= None):
            node_2 = np.int16(node_2).item()
        datasetCreator.set_selected_node2(self, node_2)  
        ## the relation itself: 
        ## node 2 id is added to is part of field of node 1
        add_relation = st.button("Add Relation", key="add_relation_ha")
        if(add_relation):
            for i in range(len(self.df.index)):
                n_id = self.df["identifier"][i]
                if(n_id == node_1): # find node 1
                    self.df["isPartOf"][i] = node_2
                    break
        self.df.to_csv(self.file_name, index=False)

    def __add_relation_assesses(self, node_1):
        ## node 1 is rER and 2 nodes must be aER
        aER_list = []; node_2 = None
        for i in range(len(self.df.index)):
            node_title = self.df["title"][i]
            node_type = self.df["type"][i]
            if(node_type == "aER"):
                aER_list.append(node_title)
        title_selector = st.selectbox("Select aER you want to assess", set(aER_list), key="find_node2_assess_relation")
        title_has_duplicate = datasetCreator.__title_has_duplicate(title_selector, aER_list)
        id_selector = ""
        if title_has_duplicate:
            id_list = []
            for i in range(len(self.df.index)):
                node_id = self.df["identifier"][i]
                node_title = self.df["title"][i]
                node_type = self.df["type"][i]
                if node_type == "aER":
                     if(title_selector == node_title): id_list.append(node_id)
            id_selector = st.selectbox("Select ID: ", id_list, key="find_node2_id_relation", disabled= False)    
        if(id_selector): node_2 = int(id_selector)
        else:
            #if node is unique --> no id selector --> find id
            for i in range(len(self.df.index)):
                node_id = self.df["identifier"][i]
                node_title = self.df["title"][i]
                node_type = self.df["type"][i]
                if node_type == "aER":
                    if(title_selector == node_title): node_2 = node_id
        if(node_2!= None):
            node_2 = np.int16(node_2).item()
        datasetCreator.set_selected_node2(self, node_2) 
        ## the relation itself: 
        ## the node_1 is added to “assesses” field of node with id  node_2.
        add_relation = st.button("Add Relation", key="add_relation_ha")
        if(add_relation):
            #one to one --> check if any other node refers to node_2 in assesses
            for j in range(len(self.df.index)):
                try: assess = int(self.df["assesses"][j] )
                except: assess = None
                if(assess != None and assess == node_2): 
                    self.df["assesses"][j] = ""
            for i in range(len(self.df.index)):
                n_id = self.df["identifier"][i]
                if(n_id == node_1): # find node 1
                    self.df["assesses"][i] = node_2
                    break
            self.df.to_csv(self.file_name, index=False)
    
    def __add_relation_isAssessedBy(self, node_1):
        rER_list = []; node_2 = None
        for i in range(len(self.df.index)):
            node_title = self.df["title"][i]
            node_type = self.df["type"][i]
            if(node_type == "rER"):
                rER_list.append(node_title)
        title_selector = st.selectbox("Select rER", set(rER_list), key="find_node2_isb_relation", disabled= False)
        title_has_duplicate = datasetCreator.__title_has_duplicate(title_selector, rER_list)
        id_selector = ""
        if title_has_duplicate:
            id_list = []
            for i in range(len(self.df.index)):
                node_id = self.df["identifier"][i]
                node_title = self.df["title"][i]
                node_type = self.df["type"][i]
                if node_type == "rER":
                     if(title_selector == node_title): id_list.append(node_id)
            id_selector = st.selectbox("Select ID: ", id_list, key="find_node2_id_relation", disabled= False)    
        if(id_selector): node_2 = int(id_selector)
        else:
            #if node is unique --> no id selector --> find id
            for i in range(len(self.df.index)):
                node_id = self.df["identifier"][i]
                node_title = self.df["title"][i]
                node_type = self.df["type"][i]
                if node_type == "rER":
                    if(title_selector == node_title): node_2 = node_id
        if(node_2!= None):
            node_2 = np.int16(node_2).item()
        datasetCreator.set_selected_node2(self, node_2) 
         ## the relation itself: 
        ## the node_1 is added to “assesses” field of node with id  node_2.
        add_relation = st.button("Add Relation", key="add_relation_ha")
        if(add_relation):
             ## is Assessed by is one to one --> check if any other node refers to node_1 in assesses
                ## and if it does then set this field to empty
            for j in range(len(self.df.index)):
                try: assess = int(self.df["assesses"][j] )
                except: assess = None
                if(assess != None and assess == node_1): 
                    self.df["assesses"][j] = ""
            for i in range(len(self.df.index)):
                n_id = self.df["identifier"][i]
                if(n_id == node_2): # find node 2
                    self.df["assesses"][i] = node_1
                    break
            self.df.to_csv(self.file_name, index=False)

    def __add_relation_HasPart(self, node_1):
        # Has Part is only possible if node 1 is composite and node 2 is atomic
        # so the only possible options for node 2 are atomics ER
        atomic_title_list = []; node_2 = None
        for i in range(len(self.df.index)):
            node_title = self.df["title"][i]
            node_type = self.df["type"][i]
            if(node_type != "start" and node_type != "end" and node_type != "iER" and node_type != "rER" and node_type != "aER"):
                atomic_title_list.append(node_title)
        title_selector = st.selectbox("Select atomic ER", set(atomic_title_list), key="find_node2_ha_relation", disabled= False)
        # find type or types based on title
        title_has_duplicate = datasetCreator.__title_has_duplicate(title_selector, atomic_title_list)
        node_has_duplicate = False
        type_selector  = ""
        if title_has_duplicate: 
            type_list = []
            for i in range(len(self.df.index)):
                node_title = self.df["title"][i]
                node_type = self.df["type"][i]
                if (node_title == title_selector):
                    if(node_type != "start" and node_type != "end" and node_type != "iER" and node_type != "rER" and node_type != "aER"):
                        type_list.append(node_type)
            type_selector = st.selectbox("Select ER type", set(type_list))
            node_has_duplicate = datasetCreator.__title_has_duplicate(type_selector, type_list)    
        # if the there are duplicate titles (there can be duplicate nodes --> only IDs are unique) then we need id field to find 
        # the correct node
        id_selector = ""
        if( node_has_duplicate):
            id_list = []
            for i in range(len(self.df.index)):
                node_id = self.df["identifier"][i]
                node_title = self.df["title"][i]
                node_type = self.df["type"][i]
                if(node_type == type_selector):
                     if(title_selector == node_title): id_list.append(node_id)
            id_selector = st.selectbox("Select ID: ", id_list, key="find_node2_id_relation", disabled= False)    
        if(id_selector): node_2 = int(id_selector)
        else:
            #if node is unique --> no id selector --> find id
            for i in range(len(self.df.index)):
                node_id = self.df["identifier"][i]
                node_title = self.df["title"][i]
                node_type = self.df["type"][i]
                if type_selector == "":
                    if title_selector == node_title: 
                        if(node_type != "start" and node_type != "end" and node_type != "iER" and node_type != "rER" and node_type != "aER"):    
                            node_2 = node_id
                else:
                    if(node_type == type_selector and title_selector == node_title): node_2 = node_id
        if(node_2!= None):
            node_2 = np.int16(node_2).item()
        datasetCreator.set_selected_node2(self, node_2)  
        ## the relation itself: 
        ## node 1 id is added to is part of field of node 2
        add_relation = st.button("Add Relation", key="add_relation_ha")
        if(add_relation):
            for i in range(len(self.df.index)):
                n_id = self.df["identifier"][i]
                if(n_id == node_2): # find node 2
                    self.df["isPartOf"][i] = node_1
                    break
        self.df.to_csv(self.file_name, index=False)

    def __add_relation_comesAfter(self, node_1):
            type_list = []; node_2 = None
            type_list = ["All",'start','iER', 'aER']
            type_select = st.selectbox("Select the ER type", type_list, key="find_node2_type_relation", disabled=False)
            ier_title_list = []; aer_title_list = []; all_title_list = []
            if(type_select == "start"):
                node_2 = 0
            else:
                #add start node to all:
                all_title_list.append(self.df["title"][0])
                # adding aer and ier to their respective lists excluding the node 1   
                for i in range(len(self.df.index)):
                    node_id = self.df["identifier"][i]
                    node_title = self.df["title"][i]
                    node_type = self.df["type"][i]
                    if( node_id != node_1):
                        if(node_type == "iER"): 
                            ier_title_list.append(node_title)
                            all_title_list.append(node_title) 
                        elif(node_type == "aER"):
                            aer_title_list.append(node_title)
                            all_title_list.append(node_title)
                title_has_duplicate = False 
                if(type_select == "All"): 
                    title_selector = st.selectbox("Select ER", set(all_title_list), key="find_node2_title_relation", disabled= False)
                    title_has_duplicate = datasetCreator.__title_has_duplicate(title_selector, all_title_list)    
                elif(type_select == "iER"): 
                    title_selector = st.selectbox("Select ER", set(ier_title_list), key="find_node2_title_relation", disabled= False)
                    title_has_duplicate = datasetCreator.__title_has_duplicate(title_selector, ier_title_list)
                elif(type_select == "aER"): 
                    title_selector = st.selectbox("Select ER", set(aer_title_list), key="find_node2_title_relation", disabled= False)
                    title_has_duplicate = datasetCreator.__title_has_duplicate(title_selector, aer_title_list) 
                
                # #if the there are duplicate titles (there can be duplicate nodes --> only IDs are unique) then we need id field to find 
                # # the corret node
                id_selector = ""
                if(title_has_duplicate):
                    id_list = []
                    for i in range(len(self.df.index)):
                        node_id = self.df["identifier"][i]
                        node_title = self.df["title"][i]
                        node_type = self.df["type"][i]
                        if(type_select == "All"):
                            if(title_selector == node_title): id_list.append(node_id)
                        else:
                            if(type_select == node_type and title_selector == node_title): id_list.append(node_id)
                    id_selector = st.selectbox("Select ID: ", id_list, key="find_node2_id_relation", disabled= False)    
                if(id_selector): node_2 = int(id_selector)
                else:
                    #if node is unique --> no id selector --> find id
                    for i in range(len(self.df.index)):
                        node_id = self.df["identifier"][i]
                        node_title = self.df["title"][i]
                        node_type = self.df["type"][i]
                        if(type_select == "All"):
                            if node_type == "aER" or node_type=="iER" or node_type =="start":
                                if(title_selector == node_title): node_2 = node_id
                        else:
                            if(type_select == node_type and title_selector == node_title): node_2= node_id
            if(node_2!= None):
                node_2 = np.int16(node_2).item()
            datasetCreator.set_selected_node2(self, node_2)

            # find the node with `comesAfter` == node2 --> change this field to node1
            add_relation = st.button("Add Relation", key="add_relation")
            if(add_relation):
                node1_has_CA = datasetCreator.__node_has_CA(self, node_1)
                # print(node1_has_CA)
                node1_is_referred_ca = datasetCreator.__node_is_referred_by_other_ca(self, node_1)
                # print(node1_is_referred_ca)
                # refer to algorithm in doc
                if(node1_has_CA):
                    if(node1_is_referred_ca): #case 4
                        # node_comesAfter_node1's CA = node1's CA
                        # find node_1's ca in df"
                        for i in range(len(self.df.index)):
                            node_id = self.df["identifier"][i]
                            if(node_id == node_1): #found node_1
                                node1_ca = self.df["comesAfter"][i] # found node1's ca
                                for j in range(len(self.df.index)): # look for the node that refers node 1
                                    try: ca = int(self.df["comesAfter"][j])
                                    except: ca = None
                                    if(ca != None and ca == node_1): # found the node that comesAFter node1
                                        # change this node's ca to node1's ca
                                        self.df["comesAfter"][j] = node1_ca
                                        self.df.to_csv(self.file_name, index=False)
                                        break 
                                break
                    # node_comesAfter_node2's CA = node1's ID
                    # look for the node that refers node 2
                    for i in range(len(self.df.index)):
                        try: ca = int(self.df["comesAfter"][i])
                        except: ca = None
                        if(ca != None and ca == node_2): # found the node that comesAFter node1
                            # change this node's ca to node1's ca
                            self.df["comesAfter"][i] = node_1
                            self.df.to_csv(self.file_name, index=False)
                            break             
                else:
                    if(node1_is_referred_ca): # case 2
                        # find the last node in the chain starting with node_1 where node 1 does not come after anything
                        y = datasetCreator.__find_last_node_in_chain(self, node_1) 
                        # node_comesAfter_node2's CA = y
                        # look for the node that refers node 2
                        for i in range(len(self.df.index)):
                            try: ca = int(self.df["comesAfter"][i])
                            except: ca = None
                            if(ca != None and ca == node_2): # found the node that comesAFter node1
                                # change this node's ca to node1's ca
                                self.df["comesAfter"][i] = y
                                self.df.to_csv(self.file_name, index=False)
                                break 
                        pass
                    else:
                        # node_comesAfter_node2's CA = node1's ID
                        # look for the node that refers node 2
                        for i in range(len(self.df.index)):
                            try: ca = int(self.df["comesAfter"][i])
                            except: ca = None
                            if(ca != None and ca == node_2): # found the node that comesAFter node1
                                # change this node's ca to node1's ca
                                self.df["comesAfter"][i] = node_1
                                self.df.to_csv(self.file_name, index=False)
                                break 

                # then change node1's `comesAfter` field to node 2's id --> case 1: General case
                # algorithm in doc: Node1's CA = Node2's id
                #task: check if node 2 has ca == node 1 id and if yes remove it
                for i in range(len(self.df.index)):
                    node_id= self.df["identifier"][i]
                    if(node_id == node_1): #find node 1 in df
                        self.df["comesAfter"][i] = node_2 # set node1's ca to node 2
                        self.df.to_csv(self.file_name, index=False) # save the df
                        # if node 2's CA == node 1 --> remove it
                        for j in range(len(self.df.index)):
                            node2_id= self.df["identifier"][j]
                            if(node2_id == node_2): #find node 2
                                try: ca = int(self.df["comesAfter"][j])
                                except: ca = None
                                if(ca != None and ca == node_1):
                                    self.df["comesAfter"][j] = None
                                    self.df.to_csv(self.file_name, index=False) # save the df
                                    break
                        break
    
    # given a node id this function returns true if there is another node with id of this node in its comesAfter field
    def __node_is_referred_by_other_ca(self, node_1):
        res = False
        for i in range(len(self.df.index)):
            try: ca = int(self.df["comesAfter"][i])
            except: ca = None
            if(ca == node_1): # check if there is a comesAfter fields that refer to node_1's id
                if(ca != None): 
                    res = True
                    break
        return res

    # given a node id this function returns true if the node has a value in comesAFter field of the dataset
    def __node_has_CA(self, node_1):
        res = False
        for i in range(len(self.df.index)):
            node_id= self.df["identifier"][i]
            if(node_id == node_1): # find node_1
                try: ca = int(self.df["comesAfter"][i])
                except: ca = None
                if(ca != None): 
                    res = True
                    break
        return res
    #Recursive function to find the last node in a chain of nodes with comesAfter relation starting with given node
    def __find_last_node_in_chain(self, node):
        current_node = node
        for i in range(len(self.df.index)):
            node_comesAfter_current_node = self.df["comesAfter"][i]
            node_comesAfter_current_node_id = self.df["identifier"][i]
            if(node_comesAfter_current_node == current_node):
                current_node = node_comesAfter_current_node_id
                current_node = datasetCreator.__find_last_node_in_chain(self, current_node)
                break
        return current_node
    
    def __find_node1_for_relations(self):
        # type_col, title_col, id_col = st.columns(3)
        # # select type: there are 4 type: iER, aER, rER, atomic ER or all --> default = All
        if "confirm_ER_1" not in st.session_state:
                st.session_state.confirm_ER_1 = False
        type_selector = st.selectbox("Select the ER type", ("All",'iER', 'aER', 'rER', "atomic ER"), key="find_node1_type_relation", disabled= st.session_state.confirm_ER_1)
        # after choosing type and selectbox of unique titles is created based on the type (ordered alphabetically)
        ier_title_list = []; aer_title_list = []; rer_title_list = []; atomic_title_list = []; all_title_list = []
        for i in range(len(self.df.index)):
            node_title = self.df["title"][i]
            node_type = self.df["type"][i]
            if(node_type != "start" and node_type != "end"):
                all_title_list.append(node_title)
                if(node_type == "iER"): ier_title_list.append(node_title) 
                elif(node_type == "aER"):aer_title_list.append(node_title)
                elif(node_type =="rER"):rer_title_list.append(node_title)
                else:atomic_title_list.append(node_title)
        title_has_duplicate = False
        if(type_selector == "All"): 
            title_selector = st.selectbox("Select ER", set(all_title_list), key="find_node1_title_relation", disabled= st.session_state.confirm_ER_1)
            title_has_duplicate = datasetCreator.__title_has_duplicate(title_selector, all_title_list)    
        elif(type_selector == "iER"): 
            title_selector = st.selectbox("Select ER", set(ier_title_list), key="find_node1_title_relation", disabled= st.session_state.confirm_ER_1)
            title_has_duplicate = datasetCreator.__title_has_duplicate(title_selector, ier_title_list)
        elif(type_selector == "aER"): 
            title_selector = st.selectbox("Select ER", set(aer_title_list), key="find_node1_title_relation", disabled= st.session_state.confirm_ER_1)
            title_has_duplicate = datasetCreator.__title_has_duplicate(title_selector, aer_title_list) 
        elif(type_selector == "rER"): 
            title_selector = st.selectbox("Select ER", set(rer_title_list), key="find_node1_title_relation", disabled= st.session_state.confirm_ER_1)
            title_has_duplicate = datasetCreator.__title_has_duplicate(title_selector, rer_title_list)
        elif(type_selector == "atomic ER"): 
            title_selector = st.selectbox("Select ER", set(atomic_title_list), key="find_node1_title_relation", disabled= st.session_state.confirm_ER_1)
            title_has_duplicate = datasetCreator.__title_has_duplicate(title_selector, atomic_title_list)
        #if the there are duplicate titles (there can be duplicate nodes --> only IDs are unique) then we need id field to find 
        # the corret node
        id_selector = ""; atomic_type_selector  = ""
        if(type_selector != "atomic ER"):
            if(title_has_duplicate):
                id_list = []
                for i in range(len(self.df.index)):
                    node_id = self.df["identifier"][i]
                    node_title = self.df["title"][i]
                    node_type = self.df["type"][i]
                    if(type_selector == "All" or type_selector == "atomic ER"):
                        if(title_selector == node_title): id_list.append(node_id)
                    else:
                        if(type_selector == node_type and title_selector == node_title): id_list.append(node_id)
                id_selector = st.selectbox("Select ID: ", id_list, key="find_node1_id_relation", disabled= st.session_state.confirm_ER_1)    
        else:
            node_has_duplicate = False
            if title_has_duplicate: 
                type_list = []
                for i in range(len(self.df.index)):
                    node_title = self.df["title"][i]
                    node_type = self.df["type"][i]
                    node_id = self.df["identifier"][i]
                    # if(node_id != node_1):  
                    if (node_title == title_selector):
                        if(node_type != "start" and node_type != "end" and node_type != "iER" and node_type != "rER" and node_type != "aER"):
                            type_list.append(node_type)
                atomic_type_selector = st.selectbox("Select ER type", set(type_list))
                node_has_duplicate = datasetCreator.__title_has_duplicate(atomic_type_selector, type_list) 
            if( node_has_duplicate):
                id_list = []
                for i in range(len(self.df.index)):
                    node_id = self.df["identifier"][i]
                    node_title = self.df["title"][i]
                    node_type = self.df["type"][i]
                    # if(node_id != node_1):  
                    if(node_type == atomic_type_selector):
                            if(title_selector == node_title): id_list.append(node_id)
                id_selector = st.selectbox("Select ID: ", id_list, key="find_node2_id_relation", disabled= False) 
        
        if(id_selector): return int(id_selector)
        else:
            #if node is unique --> no id selector --> find id
            for i in range(len(self.df.index)):
                node_id = self.df["identifier"][i]
                node_title = self.df["title"][i]
                node_type = self.df["type"][i]
                if(type_selector == "All"):
                    if(title_selector == node_title): return node_id
                elif type_selector == "atomic ER":
                    if atomic_type_selector == "":
                        if title_selector == node_title: 
                            if(node_type != "start" and node_type != "end" and node_type != "iER" and node_type != "rER" and node_type != "aER"):    
                                return node_id
                    else:
                            if(node_type == atomic_type_selector and title_selector == node_title): return node_id
                else:
                    if(type_selector == node_type and title_selector == node_title): return node_id
                # print(type_selector)
    def __create_node_addition_fields(self):
        adder = st.container()
        node_title = ""
        node_type = ""
        node_des = ""
        node_url = ""
        node_dur = 0
        node_type_select = ""
        node = []
        with adder:
            # title
            st.subheader("Add a New Node")
            #necessary data
            disable = False
            if "Save_node" in st.session_state:
                disable = st.session_state.Save_node
            if "add_next" in st.session_state:
                disable = not st.session_state.add_next
                if (not disable): st.session_state.add_node_title = ""
            must_input  = False
            title_col, ER_col, atomic_col = st.columns([1.75,0.875,0.875])
            with title_col:
                node_title = st.text_input("Title", key="add_node_title", disabled=disable)
            with ER_col:
                if(node_title !=""):
                    must_input = True
                    node_type_select = st.selectbox("ER type", ('iER', 'aER', 'rER', "atomic ER"), disabled=disable)
                    node_type = node_type_select
                    if(node_type_select == "atomic ER"):
                        with atomic_col:
                            atomic_type = st.selectbox("atomic type", ('.png', '.jpeg', '.mov', '.mp4', '.exe', '.ipynd', '.app', '.mp3', '.wav', '.txt', '.pdf', '.html', '.md', '.pptx', '.dvi', '.csv', '.xlsx', '.zip' ), disabled=disable)
                            node_type = atomic_type
            if(must_input):
                if(node_type=="iER" or node_type=="aER" or node_type=="rER"):
                    des_col, url_col= st.columns(2)
                    with des_col:
                        node_des = st.text_input("Description", disabled=disable)
                    with url_col:
                        node_url = st.text_input("URL", disabled=disable)
                else:
                    des_col, url_col, dur_col = st.columns(3)
                    with des_col:
                        node_des = st.text_input("Description", disabled=disable)
                    with url_col:
                        node_url = st.text_input("URL", disabled=disable)
                    with dur_col:
                        node_dur = st.number_input('Duration', value = 2, disabled=disable)
            if(node_des!="" or node_url!=""):
                col1, col2 = st.columns([1, 8])
                with col1:
                    add_node = st.button("Save", key="Save_node", disabled=disable)
                if(add_node):
                    new_id = self.df["identifier"][len(self.df.index)-1]
                    if(new_id != None):
                        new_id = np.int16(new_id).item()
                    node = [new_id,node_title,node_des,node_url,node_type,'','','','','','','',node_dur]
                    datasetCreator.set_selected_node(self, new_id)
                with col2:
                    if(disable):
                        add_new_node = st.button("Add another node", key="add_next")
        return node                  
    def __reset_field_after_node_saved(self):
       print( st.session_state.add_node_title)
    # this function return id of node for editing purposes
    def __find_node_list(self):   
        type_col, title_col, id_col = st.columns(3)
        # select type: there are 4 type: iER, aER, rER, atomic ER or all --> default = All
        with type_col:
            disable = False
            if "confirm_edit" in st.session_state:
                disable = st.session_state.confirm_edit
            type_selector = st.selectbox("Select the ER type", ("All",'iER', 'aER', 'rER', "atomic ER"), disabled=disable)
        # after choosing type and selectbox of unique titles is created based on the type (ordered alphabetically)
        with title_col:
            ier_title_list = []; aer_title_list = []; rer_title_list = []; atomic_title_list = []; all_title_list = []
            for i in range(len(self.df.index)):
                node_title = self.df["title"][i]
                node_type = self.df["type"][i]
                if(node_type != "start" and node_type != "end"):
                    all_title_list.append(node_title)
                    if(node_type == "iER"): ier_title_list.append(node_title) 
                    elif(node_type == "aER"):aer_title_list.append(node_title)
                    elif(node_type =="rER"):rer_title_list.append(node_title)
                    else:atomic_title_list.append(node_title)
            title_has_duplicate = False
            if(type_selector == "All"): 
                title_selector = st.selectbox("Select ER", set(all_title_list), disabled=disable, key="find_node_title")
                title_has_duplicate = datasetCreator.__title_has_duplicate(title_selector, all_title_list)    
            elif(type_selector == "iER"): 
                title_selector = st.selectbox("Select ER", set(ier_title_list),  disabled=disable, key="find_node_title")
                title_has_duplicate = datasetCreator.__title_has_duplicate(title_selector, ier_title_list)
            elif(type_selector == "aER"): 
                title_selector = st.selectbox("Select ER", set(aer_title_list),  disabled=disable, key="find_node_title")
                title_has_duplicate = datasetCreator.__title_has_duplicate(title_selector, aer_title_list) 
            elif(type_selector == "rER"): 
                title_selector = st.selectbox("Select ER", set(rer_title_list),  disabled=disable, key="find_node_title")
                title_has_duplicate = datasetCreator.__title_has_duplicate(title_selector, rer_title_list)
            elif(type_selector == "atomic ER"): 
                title_selector = st.selectbox("Select ER", set(atomic_title_list),  disabled=disable, key="find_node_title")
                title_has_duplicate = datasetCreator.__title_has_duplicate(title_selector, atomic_title_list)
        #if the there are duplicate titles (there can be duplicate nodes --> only IDs are unique) then we need id field to find 
        # the corret node
        with id_col:
            id_selector = ""
            if(title_has_duplicate):
                id_list = []
                for i in range(len(self.df.index)):
                    node_id = self.df["identifier"][i]
                    node_title = self.df["title"][i]
                    node_type = self.df["type"][i]
                    if(type_selector == "All" or type_selector == "atomic ER"):
                        if(title_selector == node_title): id_list.append(node_id)
                    else:
                        if(type_selector == node_type and title_selector == node_title): id_list.append(node_id)
                id_selector = st.selectbox("Select ID: ", id_list,  disabled=disable)    
        if(id_selector):
            return int(id_selector)
        else:
            #if node is unique --> no id selector --> find id
            for i in range(len(self.df.index)):
                node_id = self.df["identifier"][i]
                node_title = self.df["title"][i]
                node_type = self.df["type"][i]
                if(type_selector == "All"):
                    if(title_selector == node_title): return node_id
                elif type_selector == "atomic ER": 
                    if(node_type != "aER" and node_type!="iER" and node_type != "rER"):
                       if(title_selector == node_title): return node_id 
                else:
                    if(type_selector == node_type and title_selector == node_title): return node_id

    def __edit_option(self, n_id):
        if n_id == None: return None
        node = datasetCreator.__get_node_from_id(self, n_id)
        old_title = node["title"]
        old_type = node["type"]
        old_des = str(node["des"])
        if(old_des == "nan"): old_des =""
        old_url = str(node["url"])
        if( old_url  == "nan"):  old_url  =""
        old_dur = int(node["dur"])

        new_node_title = ""
        new_node_type = ""
        new_node_des = ""
        new_node_url = ""
        new_node_dur = 0
        node_type_select = ""
        node = []
        must_input = False
        title_col, ER_col, atomic_col = st.columns([1.75,0.875,0.875])
        disable = False
        if("delete_node" in st.session_state):
            if(st.session_state.delete_node == True):
                disable = True
        with title_col:
            new_node_title = st.text_input("Title", value=old_title, disabled=disable, key = "new_edit_node_title")
        with ER_col:
            if(new_node_title !=""):
                must_input = True
                ER_list = datasetCreator.__get_ER_list_for_edit(self, old_type)
                ER_type = old_type
                # if er type is one of the atomic, then it is changed to "atomic ER"
                if(ER_type!= "iER" and ER_type != "aER" and ER_type !="rER"): ER_type = "atomic ER"
                ER_index = 0; 
                for e in ER_list:
                    if e == ER_type: ER_index = ER_list.index(e)
                node_type_select = st.selectbox("ER type", ER_list, index=ER_index, key="node_type_select", disabled=disable)
                new_node_type = node_type_select
                if(new_node_type == "atomic ER"):
                    with atomic_col:
                        atomic_ER_list = ['.png', '.jpeg', '.mov', '.mp4', '.exe', '.ipynd', '.app', '.mp3', '.wav', '.txt', '.pdf', '.html', '.md', '.pptx', '.dvi', '.csv', '.xlsx', '.zip']
                        atomic_ER_index = 0
                        for e in atomic_ER_list:
                            if e == old_type: atomic_ER_index = atomic_ER_list.index(e)
                        atomic_type = st.selectbox("atomic type", atomic_ER_list, index = atomic_ER_index, disabled=disable)
                        new_node_type = atomic_type

        if(must_input):
            if(new_node_type=="iER" or new_node_type=="aER" or new_node_type=="rER"):
                des_col, url_col= st.columns(2)
                with des_col:
                    new_node_des = st.text_input("Description", value=old_des, disabled=disable)
                with url_col:
                    new_node_url = st.text_input("URL", value=old_url, disabled=disable)
            else:
                des_col, url_col, dur_col = st.columns(3)
                with des_col:
                    new_node_des = st.text_input("Description", value=old_des, disabled=disable)
                with url_col:
                    new_node_url = st.text_input("URL", value=old_url, disabled=disable)
                with dur_col:
                    new_node_dur = st.number_input('Duration', value =old_dur, disabled=disable)
        if(new_node_des!="" or new_node_url!=""):
            #isPartOf,assesses,comesAfter,requires,alternativeContent,references,isFormatOf,duration
            is_part_of = ""; assesses = ""; ca = ""; req=""; ac = ""; ref = ""; is_format_of = ""
            for i in range(len(self.df.index)):
                n = self.df["identifier"][i]
                if n == n_id:
                    is_part_of = self.df["isPartOf"][i]; assesses = self.df["assesses"][i]; ca = self.df["comesAfter"][i]
                    req = self.df["requires"][i]; ac= self.df["alternativeContent"][i]
                    ref= self.df["references"][i]; is_format_of= self.df["isFormatOf"][i]

                    if old_type == "aER" and new_node_type != "aER":
                        # the node is not aER anymore --> remove all references to this node in assess field
                        for j in range(len(self.df.index)):
                            try: a = int(self.df["assesses"][j])
                            except: a =None
                            if a != None and a == n_id: self.df["assesses"][j] = ""
                        if new_node_type != "iER": # update comesAFter if new node is not ier ir aers
                            try: c = int(self.df["comesAfter"][i])
                            except: c = None
                            if c != None: # technically this value should not be none
                                for j in range(len(self.df.index)):
                                    try: next_ca = int(self.df["comesAfter"][j])
                                    except: next_ca = None
                                    if next_ca == n_id:
                                        # print(next_ca)
                                        self.df["comesAfter"][j] = c
                                        ca = ""
                            if new_node_type != "rER": ## new node is atomic then remove any reference in ispart of other ndoes
                                for j in range(len(self.df.index)):
                                    try: a = int(self.df["isPartOf"][j])
                                    except: a =None
                                    if a != None and a == n_id: self.df["isPartOf"][j] = ""
                    if old_type == "iER" and new_node_type != "iER":
                        # two relations: comesAfter, isPartof
                        # if new node is aER nothing is affected
                        # if new node is atomic or rER then we need to update comesAfter
                        if new_node_type != "aER":
                            try: c = int(self.df["comesAfter"][i])
                            except: c = None
                            if c != None: # technically this value should not be none
                                for j in range(len(self.df.index)):
                                    try: next_ca = int(self.df["comesAfter"][j])
                                    except: next_ca = None
                                    if next_ca == n_id:
                                        # print(next_ca)
                                        self.df["comesAfter"][j] = c
                                        ca = ""
                            if new_node_type != "rER": ## new node is atomic then remove any reference in ispart of other ndoes
                                for j in range(len(self.df.index)):
                                    try: a = int(self.df["isPartOf"][j])
                                    except: a =None
                                    if a != None and a == n_id: self.df["isPartOf"][j] = ""
                    if old_type == "rER" and new_node_type != "rER":
                        # if node type is changed from rER to something that is not rER --> remove assesses field from this node
                        assesses = ""
                        if new_node_type != "iER" and new_node_type !="aER": # new type is atomic --> remove isPArtOf references
                            for j in range(len(self.df.index)):
                                    try: a = int(self.df["isPartOf"][j])
                                    except: a =None
                                    if a != None and a == n_id: self.df["isPartOf"][j] = ""
                    old_is_atomic = old_type != "iER" and old_type != "aER" and old_type != "rER"
                    new_is_atomic = new_node_type != "iER" and new_node_type != "aER" and new_node_type != "rER"
                    if old_is_atomic and not new_is_atomic:
                        #if new type is not atomic --> remove ispartof this node
                        is_part_of = ""
                        ## update requires
                        # set req of node itself to empty
                        req = ""
                        # remove requires of any node that refers to this node in their req
                        for i in range(len(self.df.index)):
                            require_ids = self.df["requires"][i]
                            require_id_list = []
                            if type(require_ids) != str: require_ids = str(require_ids)
                            if type(require_ids) == str and require_ids!="":
                                require_id_list = require_ids.split(",") # convert node's requires to list
                                for n in require_id_list: 
                                    try: n_int = int(n)
                                    except: 
                                        try: n_int = int(float(n))
                                        except: n_int = None
                                    if n_int == n_id :  # node exist in required field of this node 
                                        require_id_list.remove(str(n))
                                        delimiter = ','
                                        res = delimiter.join(require_id_list)
                                        self.df["requires"][i] = res
                    break
            node = [n_id ,new_node_title, new_node_des,new_node_url,new_node_type,is_part_of,assesses,ca,req,ac,ref,is_format_of,new_node_dur]
            
        return node

   
    def __get_atomic_ER_list_for_edit(self, old_type):
        atomic_ers = ['.png', '.jpeg', '.mov', '.mp4', '.exe', '.ipynd', '.app', '.mp3', '.wav', '.txt', '.pdf', '.html', '.md', '.pptx', '.dvi', '.csv', '.xlsx', '.zip']
        res = []
        res.append(old_type)
        for er in atomic_ers:
            if er not in res: res.append(er)
        return res

    def __get_ER_list_for_edit(self, node_type):
        t = node_type
        er = []
        if(t == "iER" or t == "aER" or t =="rER"): er.append(t)
        else: 
            t = "atomic ER"
            er.append(t)
        if "iER" not in er: er.append("iER")
        if "aER" not in er: er.append("aER")
        if "rER" not in er: er.append("rER")
        if "atomic ER" not in er: er.append("atomic ER")
        return er

    def __get_node_from_id(self, n_id):
        node = {}
        for i in range(len(self.df.index)):
            node_id = self.df["identifier"][i]
            node_title = self.df["title"][i]
            node_type = self.df["type"][i]
            node_des = self.df["description"][i]
            node_url = self.df["url"][i]
            node_dur = self.df["duration"][i]
            if(node_id == n_id):
                node["id"] = node_id; node["title"] = node_title; node["type"] = node_type; node["des"] = node_des
                node["url"] = node_url; node["dur"] = node_dur
                break; 
        return node

    def __title_has_duplicate(title, title_list):
        count = 0
        title_has_duplicate = False
        for t in title_list:
            if(t == title): count = count + 1
        if count > 1: title_has_duplicate = True
        return title_has_duplicate
    def print_df(self):
        print(self.df)
    def set_selected_node(self, node_id):
        self.selected_node_id = node_id
    def get_selected_node(self):
        return self.selected_node_id
    def set_selected_node2(self, node_id):
        self.selected_node2_id = node_id
    def get_selected_node2(self):
        return self.selected_node2_id