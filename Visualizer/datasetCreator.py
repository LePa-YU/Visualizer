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
        # res = False
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
        node = datasetCreator.__find_node_list(self)
        if(node != None):
            node = np.int16(node).item()
        datasetCreator.set_selected_node(self, node)
        confirm_node_btn = st.checkbox("Confirm Selection", key="confirm_edit")
        if(confirm_node_btn): 
            edited_node = datasetCreator.__edit_option(self, node)
            
        # else: datasetCreator.set_selected_node(self, None)
    
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

        new_node_title = ""
        new_node_type = ""
        new_node_des = ""
        new_node_url = ""
        new_node_dur = 0
        node_type_select = ""
        node = []
        must_input = False
        title_col, ER_col, atomic_col = st.columns([1.75,0.875,0.875])
        with title_col:
            new_node_title = st.text_input("Title", value=old_title)
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
                print(ER_type)
                node_type_select = st.selectbox("ER type", ER_list, index=ER_index, key="node_type_select") # bug
                new_node_type = node_type_select
                
                print(new_node_type)
                if(new_node_type == "atomic ER"):
                    with atomic_col:
                        atomic_ER_list = ['.png', '.jpeg', '.mov', '.mp4', '.exe', '.ipynd', '.app', '.mp3', '.wav', '.txt', '.pdf', '.html', '.md', '.pptx', '.dvi', '.csv', '.xlsx', '.zip']
                        atomic_ER_index = 0
                        for e in atomic_ER_list:
                            if e == old_type: atomic_ER_index = atomic_ER_list.index(e)
                        atomic_type = st.selectbox("atomic type", atomic_ER_list, index = atomic_ER_index)
                        new_node_type = atomic_type

                # if(new_node_type == "atomic ER"):
                #     with atomic_col:
                #         atomic_type = st.selectbox("atomic type", ('.png', '.jpeg', '.mov', '.mp4', '.exe', '.ipynd', '.app', '.mp3', '.wav', '.txt', '.pdf', '.html', '.md', '.pptx', '.dvi', '.csv', '.xlsx', '.zip' ))
                #"         new_node_type = atomic_type

            if(must_input):
                pass
        #         if(node_type=="iER" or node_type=="aER" or node_type=="rER"):
        #             des_col, url_col= st.columns(2)
        #             with des_col:
        #                 node_des = st.text_input("Description")
        #             with url_col:
        #                 node_url = st.text_input("URL")
        #         else:
        #             des_col, url_col, dur_col = st.columns(3)
        #             with des_col:
        #                 node_des = st.text_input("Description")
        #             with url_col:
        #                 node_url = st.text_input("URL")
        #             with dur_col:
        #                 node_dur = st.number_input('Duration', value = 2)
        #     if(node_des!="" or node_url!=""):
        #         add_node = st.button("Save")
        #         if(add_node):
        #             node = [len(self.df.index)-1,node_title,node_des,node_url,node_type,'','','','','','','',node_dur]
        return node

    def __reset_edit_ER_confirm_checkbox(ER_type):
        st.session_state.selection = ER_type
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