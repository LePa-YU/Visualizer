import os
import streamlit as st
import pandas as pd

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
        node_list = datasetCreator.__find_node_list(self)
        # conf_btn = st.button("confirm selection")
        # i = 0
        # node_id = node_list[i]
        # while(not conf_btn ):
        #     node_id = node_list[i]
        #     i = i + 1
        # if(conf_btn): datasetCreator.set_selected_node(node_id)

        # print(node_list)
    def __find_node_list(self):
        node_id_list = []    
        type_col, title_col = st.columns(2)
        # select type:
        with type_col:
            type_selector = st.selectbox("Select the ER type", ("All",'iER', 'aER', 'rER', "atomic ER"))
        #search by title
        #get iER titles
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
            title_selector = ""
            title_has_duplicate = False
            if(type_selector == "All"): title_selector = st.selectbox("Select ER", all_title_list)    
            elif(type_selector == "iER"): 
                title_selector = st.selectbox("Select ER", ier_title_list)
                
            elif(type_selector == "aER"): title_selector = st.selectbox("Select ER", aer_title_list) 
            elif(type_selector == "rER"): title_selector = st.selectbox("Select ER", rer_title_list)
            elif(type_selector == "atomic ER"): title_selector = st.selectbox("Select ER", atomic_title_list)

            id_selector = ""

        for i in range(len(self.df.index)):
            # this is not going to work --> the title and type are not unique and user cannot see the ids ( the only unique)
            # needs somes sort of visual to ensure the correct node is being edited
            node_id = self.df["identifier"][i]
            node_title = self.df["title"][i]
            node_type = self.df["type"][i]
            if(type_selector == "All" or type_selector == "atomic ER"):
                if(title_selector == node_title): node_id_list.append(node_id)
            else:
                if(type_selector == node_type and title_selector == node_title):
                    node_id_list.append(node_id)
            
        return node_id_list
                      
    
    def print_df(self):
        print(self.df)
    def set_selected_node(self, node_id):
        self.selected_node_id = node_id
    def get_selected_node(self):
        return self.selected_node_id
