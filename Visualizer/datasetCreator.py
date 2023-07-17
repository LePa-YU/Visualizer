import os
import streamlit as st
import pandas as pd
import numpy as np

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
            must_input  = False
            title_col, ER_col, atomic_col = st.columns([1.75,0.875,0.875])
            with title_col:
                node_title = st.text_input("Title")
            with ER_col:
                if(node_title !=""):
                    must_input = True
                    node_type_select = st.selectbox("ER type", ('iER', 'aER', 'rER', "atomic ER"))
                    node_type = node_type_select
                    if(node_type_select == "atomic ER"):
                        with atomic_col:
                            atomic_type = st.selectbox("atomic type", ('.png', '.jpeg', '.mov', '.mp4', '.exe', '.ipynd', '.app', '.mp3', '.wav', '.txt', '.pdf', '.html', '.md', '.pptx', '.dvi', '.csv', '.xlsx', '.zip' ))
                            node_type = atomic_type
            if(must_input):
                if(node_type=="iER" or node_type=="aER" or node_type=="rER"):
                    des_col, url_col= st.columns(2)
                    with des_col:
                        node_des = st.text_input("Description")
                    with url_col:
                        node_url = st.text_input("URL")
                else:
                    des_col, url_col, dur_col = st.columns(3)
                    with des_col:
                        node_des = st.text_input("Description")
                    with url_col:
                        node_url = st.text_input("URL")
                    with dur_col:
                        node_dur = st.number_input('Duration', value = 2)
            if(node_des!="" or node_url!=""):
                add_node = st.button("Save")
                if(add_node):
                    node = [len(self.df.index)-1,node_title,node_des,node_url,node_type,'','','','','','','',node_dur]
        return node
    
    def add_node(self):
        node = datasetCreator.__create_node_addition_fields(self)
        if(node):
            self.df.loc[len(self.df.index)-1] = node
            self.df.loc[len(self.df.index)] = [len(self.df.index),'End','end','','end','','',0,'','','','','']
            self.df.to_csv(self.file_name, index=False)
    
    def edit_node(self):
        if(len(self.df.index) <= 2):
            st.text("Dataset is empty please add a node")
        else:
            node = datasetCreator.__find_node_list(self)
            if(node != None):
                node = np.int16(node).item()
            datasetCreator.set_selected_node(self, node)
            confirm_node_btn = st.checkbox("Confirm Selection", key="confirm_edit")
            if(confirm_node_btn): 
                edited_node = datasetCreator.__edit_option(self, node)
                if(edited_node):
                    save_col, delete_col=st.columns([1, 3.5])
                    disable = False
                    if("delete_node" in st.session_state):
                        if(st.session_state.delete_node == True): disable = True
                    with save_col:
                        save_node = st.button("Save Changes", key="save_change_btn", disabled=disable)
                        if(save_node):
                            self.df.loc[node] = edited_node
                            self.df.to_csv(self.file_name, index=False)
                    with delete_col:
                        delete_node = st.button("Delete Node", key="delete_node", disabled=disable)
                        if(delete_node):
                            index = 0
                            deleted_row = False
                            for i in range(len(self.df.index)):
                                n_id = self.df["identifier"][i]
                                if(n_id == node ):
                                    index = i
                                    break
                            self.df = self.df.drop(index)
                            next_index = index+1
                            for i in range(index, len(self.df.index)):
                                self.df["identifier"][i+1] = i
                            self.df.to_csv(self.file_name, index=False)  
                       
    # this function return id of node for editing purposes
    def __find_node_list(self):   
        type_col, title_col, id_col = st.columns(3)
        # select type: there are 4 type: iER, aER, rER, atomic ER or all --> default = All
        with type_col:
            if "confirm_edit" not in st.session_state:
                st.session_state.confirm_edit = False
            type_selector = st.selectbox("Select the ER type", ("All",'iER', 'aER', 'rER', "atomic ER"), disabled=st.session_state.confirm_edit)
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
                title_selector = st.selectbox("Select ER", set(all_title_list), disabled=st.session_state.confirm_edit)
                title_has_duplicate = datasetCreator.__title_has_duplicate(title_selector, all_title_list)    
            elif(type_selector == "iER"): 
                title_selector = st.selectbox("Select ER", set(ier_title_list),  disabled=st.session_state.confirm_edit)
                title_has_duplicate = datasetCreator.__title_has_duplicate(title_selector, ier_title_list)
            elif(type_selector == "aER"): 
                title_selector = st.selectbox("Select ER", set(aer_title_list),  disabled=st.session_state.confirm_edit)
                title_has_duplicate = datasetCreator.__title_has_duplicate(title_selector, aer_title_list) 
            elif(type_selector == "rER"): 
                title_selector = st.selectbox("Select ER", set(rer_title_list),  disabled=st.session_state.confirm_edit)
                title_has_duplicate = datasetCreator.__title_has_duplicate(title_selector, rer_title_list)
            elif(type_selector == "atomic ER"): 
                title_selector = st.selectbox("Select ER", set(atomic_title_list),  disabled=st.session_state.confirm_edit)
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
                id_selector = st.selectbox("Select ID: ", id_list,  disabled=st.session_state.confirm_edit)    
        if(id_selector):
            return int(id_selector)
        else:
            #if node is unique --> no id selector --> find id
            for i in range(len(self.df.index)):
                node_id = self.df["identifier"][i]
                node_title = self.df["title"][i]
                node_type = self.df["type"][i]
                if(type_selector == "All" or type_selector == "atomic ER"):
                    if(title_selector == node_title): return node_id
                else:
                    if(type_selector == node_type and title_selector == node_title): return node_id
                      
    def __edit_option(self, n_id):
        if n_id == None: return None
        node = datasetCreator.__get_node_from_id(self, n_id)
        old_title = node["title"]
        old_type = node["type"]
        old_des = node["des"]
        if(type(old_des) != str): old_des = ""
        old_url = node["url"]
        if(type(old_url) != str): old_url = ""
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
            new_node_title = st.text_input("Title", value=old_title, disabled=disable)
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
            node = [n_id ,new_node_title, new_node_des,new_node_url,new_node_type,'','','','','','','',new_node_dur]
            
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
        # print(er)
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
