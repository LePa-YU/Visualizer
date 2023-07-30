# required imports
import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import networkx as nx
from pyvis.network import Network
import views
import requests
import Legend
import os.path
import atexit 
import csv
import os
import datasetCreator
import validity_checker

#### this file contains code for streamlit deployment
class _Customization_menu:
    def __init__(self, create_customization_menu, view):
        self.create_customization_menu = create_customization_menu
        self.view = view
    def _update_slider(start_end, atomic_min_size, atomic_max_size, ier_size, aer_size, rer_size):
        st.session_state["start_end_size"] = start_end
        st.session_state["atomic_min_size"] = atomic_min_size
        st.session_state["atomic_max_size"] = atomic_max_size
        st.session_state["ier_size"] = ier_size
        st.session_state["aer_size"] = aer_size
        st.session_state["rer_size"] = rer_size
    def _update_atomic_max_slider():
        if st.session_state.atomic_max_size  <  st.session_state.atomic_min_size:
            st.session_state.atomic_max_size  = st.session_state.atomic_min_size + 20
    def _update_atomic_min_slider():
        
        if st.session_state.atomic_max_size  <  st.session_state.atomic_min_size:
            st.session_state.atomic_max_size  = st.session_state.atomic_min_size - 20
    def create_menu(self):
        bg = "white"
        start_end_size = 20
        atomic_min_size = 10
        atomic_max_size = 30
        ier_size = 25
        aer_size = 25
        rer_size = 25
        if(self.create_customization_menu):
            with st.expander("Customization"):
                # Theme options
                # dark --> boolean -- true then background is set to black and text to white/ fasle then background is set to white and text is set to black
                st.subheader("Options:")
                colbg, colSize = st.columns([2,6])
                with colbg:
                    dark = st.checkbox("dark theme")
                    if(dark):
                        bg = "black"
                    else:
                        bg = "white"
                    self.physics = st.checkbox("physics")
                    self.resetButton = st.button('Reset Sizes')
                    if(self.resetButton):
                        _Customization_menu._update_slider(start_end_size, atomic_min_size, atomic_max_size, ier_size, aer_size, rer_size)
               
                with colSize:
                        col1, col2= st.columns(2)
                        with col1:
                            if 'atomic_max_size' not in st.session_state:
                                st.session_state['atomic_max_size'] = atomic_max_size
                            if 'atomic_min_size' not in st.session_state:
                                st.session_state['atomic_min_size'] = atomic_min_size

                            self.start_end_size = st.slider("start & end size", key="start_end_size", min_value = 0, max_value = 300, step=5, value = start_end_size, help="The start and end node size, the default is 20")
                            self.atomic_min_size = st.slider("atomic ER min size", key="atomic_min_size", min_value = 0, max_value = 300, step=5, on_change=_Customization_menu._update_atomic_max_slider(), help="The minium value of atomic ER, default is 10")
                            self.atomic_max_size = st.slider("atomic ER max size", key="atomic_max_size", min_value = 0, max_value = 300, step=5, on_change=_Customization_menu._update_atomic_min_slider(),help="The maximum value of atomic ER, default is 10")
                        with col2:
                            self.iER_size = st.slider("iER size", key="ier_size", min_value = 0, max_value = 300, step=5, value = ier_size, help="The iER node size. Note that this size is font based. The default is 25")
                            self.aER_size = st.slider("aER size", key="aer_size", min_value = 0, max_value = 300, step=5, value = aer_size, help="The aER node size. Note that this size is font based. The default is 25")
                            self.rER_size = st.slider("rER size", key="rer_size", min_value = 0, max_value = 300, step=5, value = rer_size, help="The rER node size, theW default is 25")
                    
                st.subheader("Select Colors:")
                # 7 element color options for different entities, the sencond arg is the initial color based on pumpkin color palete
                col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
                with col1:
                    aER_node_color = st.color_picker('aER node color', "#FF7273")
                with col2:
                    rER_node_color = st.color_picker('rER node color', "#FF7273")
                with col3:
                    iER_node_color = st.color_picker('iER node color', "#F69159")
                with col4:
                    general_node_color = st.color_picker('atomic node color', "#ECD19A")
                with col5:
                    assess_edge_color = st.color_picker('assess edge color', "#FF7273")
                with col6:
                    comesAfter_edge_color = st.color_picker('comes_after edge color', "#C0CB6B")
                with col7:
                    isPartOf_edge_color = st.color_picker('isPartOf edge color', "#ECD19A")
                with col8:
                    start_node_color = st.color_picker('start node color', "#C0CB6B")
                
                col9, col10, col11, col12, col13, col14, col15, col16 = st.columns(8)
                with col9:
                    end_node_color = st.color_picker('end node color', "#C0CB6B")
                with col10:
                    requires_node_color = st.color_picker('requires color', "#BF87F2")
                with col11:
                    atomic_img = st.color_picker('atomic: images', "#A24052")
                with col12:
                    atomic_mov = st.color_picker('atomic: videos', "#FBF495")   
                with col13:
                    atomic_software = st.color_picker('atomic: software', "#93C539")
                with col14:
                    atomic_audio = st.color_picker('atomic: Audio', "#437C6C") 
                with col15:
                    atomic_text = st.color_picker('atomic: text', "#20C18B")
                with col16:
                    atomic_dataset = st.color_picker('atomic: dataset', "#5FC7D3")   
                
            # set colors based on the selection
            self.view.setColors(aER_node_color, rER_node_color, iER_node_color,  general_node_color, assess_edge_color, comesAfter_edge_color, isPartOf_edge_color, start_node_color, end_node_color, requires_node_color, atomic_img, atomic_mov, atomic_software, atomic_audio, atomic_text, atomic_dataset) 
        else:
            self.view.setColors("#FF7273", "#FF7273", "#F69159", "#ECD19A", "#FF7273", "#C0CB6B", "#ECD19A", "#C0CB6B", "#C0CB6B", "#BF87F2", "#A24052", "#FBF495", "#93C539", "#437C6C", "#20C18B", "#5FC7D3")
        return bg


def __create_html_pages(label, view, bg, font_color, view1, physics, d_btn):
    view.Summative_assessment_only( bg, font_color, label, view1, physics, d_btn)
    view.Course_Overview( bg, font_color, label, view2, physics, d_btn)
    view.All_ERs( bg, font_color, label, view3, physics, d_btn)
    view.Requirements(bg, font_color, label, view4, physics, d_btn)
    view.vertical_Requirements(bg, font_color, label, view5, physics, d_btn)


def download_dataset(uploaded_file):
    dow_container = st.container(); report  = ""
    with dow_container:
        validity_file_name = uploaded_file.replace(".csv", "_validity_report.txt")
        validity = validity_checker.validity_checker(uploaded_file)
        validity.check_validity() 
        report_file = open(validity_file_name, "r")
        report = report_file.read()
        report_file.close()
        validity_report = st.expander("Please fix the following issues:") 
        with validity_report:
            st.write(report)
            if report == "": st.write("All issues are solved") 
        if os.path.getsize(validity_file_name) == 0 and report == "":
            save_file = st.checkbox("Download CSV File")
            if(save_file):
                f_name_col, down_btn_col = st.columns([2.5, 1])
                with f_name_col:
                    file_name= st.text_input("", value = uploaded_file , placeholder="What do you want to call this dataset?", label_visibility="collapsed")
                    if(file_name !=""):
                        with down_btn_col:
                            if not file_name.endswith(".csv"):
                                if "." in file_name:
                                    st.text("please remove .")
                                else:
                                    file_name = file_name + ".csv"
                            df_copy = pd.read_csv(uploaded_file)
                            csv_file = df_copy.to_csv(index=False).encode('utf-8')
                            download_btn = st.download_button(label="Download", data=csv_file, file_name=file_name, mime='text/csv')
        
    
#global variables:
uploaded_file = None
global df
# initial settings:
    # the "wide" layout allows the elements to be stretched to the size of the screen 
st.set_page_config(page_title = "LePa Visualizer", layout="wide", initial_sidebar_state="collapsed")
st.title('LePa: Learning Path Project')

# container that contains menus + visualizer --> helps with responsive attribute
container = st.container()

with container:
    # link to other dataset
    st.write("[Other datasets](https://github.com/LePa-YU/Datasets)")
    
    col1, col2, col3= st.columns([3.5, 3.5, 1])
    with col1:
        fake_ds = "FAKE1001"
        ds_2311 = "EECS 2311"
        ds_3461 = "EECS 3461"
        ds_1530 = "EECS 1530"
        ds_4462 = "EECS 4462"
        enter_own = "Custom dataset"
        dataset_options=st.selectbox('',(fake_ds, ds_2311, ds_3461, ds_1530, ds_4462, enter_own), label_visibility="collapsed")
    with col2:
        view1 = 'View 1: Summative assessment only'
        view2 = 'View 2: Course Overview'
        view3 = 'View 3: All ERs'
        view4 = "View 4: Requirements"
        view5 = "View 5: Requirements - Vertical"
        option=st.selectbox('',(view1, view2, view3, view4, view5), label_visibility="collapsed")
    
    #create layout for enter/modify data
    if dataset_options == enter_own:
        upload_col, edit_col = st.columns([3.5, 4.5])
        with edit_col:
            container_html = st.container()
    else:    
        container_html = st.container()


    if dataset_options == fake_ds:
        # get demo file from github in the Dataset repo (main) 
        url = "https://raw.githubusercontent.com/LePa-YU/Datasets/main/FAKE1001/FAKE1001.csv"
        res = requests.get(url, allow_redirects=True)
        # create a temp csv file (added to .gitignore) and copy the material from the link to this file
        with open('FAKE1001.csv','wb') as file:
            file.write(res.content)
            uploaded_file = "FAKE1001.csv"
    elif dataset_options == ds_2311:
        # get EECS 2311 file from github in the Dataset repo (main) 
        url = "https://raw.githubusercontent.com/LePa-YU/Datasets/main/EECS2311/2311_dataset_overview.csv"
        res = requests.get(url, allow_redirects=True)
        # create a temp csv file (added to .gitignore) and copy the material from the link to this file
        with open('2311_dataset_overview.csv','wb') as file:
            file.write(res.content)
            uploaded_file = "2311_dataset_overview.csv"
    elif dataset_options == ds_3461:
        # get EECS 3461 file from github in the Dataset repo (main) 
        url = "https://raw.githubusercontent.com/LePa-YU/Datasets/main/EECS3461/3461_dataset_overview.csv"
        res = requests.get(url, allow_redirects=True)
        # create a temp csv file (added to .gitignore) and copy the material from the link to this file
        with open('3461_dataset_overview.csv','wb') as file:
            file.write(res.content)
            uploaded_file = "3461_dataset_overview.csv"
    elif dataset_options == ds_1530:
        # get EECS 1530 file from github in the Dataset repo (main) 
        url = "https://raw.githubusercontent.com/LePa-YU/Datasets/main/EECS1530/1530_dataset_overview.csv"
        res = requests.get(url, allow_redirects=True)
        # create a temp csv file (added to .gitignore) and copy the material from the link to this file
        with open('1530_dataset_overview.csv','wb') as file:
            file.write(res.content)
            uploaded_file = "1530_dataset_overview.csv"
    elif dataset_options == ds_4462:
        # get EECS 4462 file from github in the Dataset repo (main) 
        url = "https://raw.githubusercontent.com/LePa-YU/Datasets/main/EECS4462/4462_dataset_overview.csv"
        res = requests.get(url, allow_redirects=True)
        # create a temp csv file (added to .gitignore) and copy the material from the link to this file
        with open('4462_dataset_overview.csv','wb') as file:
            file.write(res.content)
            uploaded_file = "4462_dataset_overview.csv"
    elif dataset_options == enter_own:
        # to write on the file browser itself
        with upload_col:
            new_dataset = "Create a new Dataset"
            existing_dataset = "Upload your dataset"
            select_options=st.selectbox('',(existing_dataset, new_dataset), label_visibility="collapsed")
            dataset = None
            if (select_options == existing_dataset):
                st.markdown(
                        """
                        <style>
                            .css-9ycgxx::before {
                                content: "Load dataset, ";
                            }
                        <style>
                        """
                , unsafe_allow_html=True)
                # user enters csv file in the file_uplader with the following properties
                u_file = st.file_uploader(label="Load Dataset:", type="csv", help = "Load your dataset  here", label_visibility= "hidden")
                if u_file is not None:
                    if(not os.path.isfile(u_file.name)):
                        with open(u_file.name,"wb") as f:
                            f.write(u_file.getbuffer())
                        # print(uploaded_file.name)
                    uploaded_file = u_file.name
                    dataset = datasetCreator.datasetCreator(u_file.name)
                   
            elif(select_options == new_dataset):
                f_name = "temp.csv"
                uploaded_file = f_name
                dataset = datasetCreator.datasetCreator(f_name)
                    # dow_container = st.container()
                    # with dow_container:
                    #     save_file = st.checkbox("Download CSV File")
                    #     if(save_file):
                    #         f_name_col, down_btn_col = st.columns([2.5, 1])
                    #         with f_name_col:
                    #             file_name= st.text_input("", placeholder="What do you want to call this dataset?", label_visibility="collapsed")
                    #             if(file_name !=""):
                    #                 with down_btn_col:
                    #                     file_name = file_name + ".csv"
                    #                     csv_file = df.to_csv(index=False).encode('utf-8')
                    #                     download_btn = st.download_button(label="Download", data=csv_file, file_name=file_name, mime='text/csv')
        #new df_container
            new_df_container = st.container()
            with new_df_container:
                if dataset!=None:
                    st.divider()
                    node_option = st.radio("What do you want to do?", ("Add a new ER", "Update a ER", "Modify Relations"), key="node_tab")
                    if(node_option == "Add a new ER"):
                            dataset.add_node()
                            download_dataset(uploaded_file)
                    elif(node_option == "Update a ER"):
                            dataset.edit_node()
                            download_dataset(uploaded_file)
                    # df = pd.read_csv(f_name)
                    if(node_option == "Modify Relations"):
                            dataset.add_relation()
                            download_dataset(uploaded_file)
                
                    
                # if "disabled" not in st.session_state:
                #     st.session_state["disabled"] = False
                # f_name = ""
                # f_name_col, change_f_name_col = st.columns([2.5, 1])

                # with f_name_col:
                #     f_name= st.text_input("Enter file name:", disabled=st.session_state.disabled, on_change=disable_file_name, placeholder="What do you want to call this dataset?", label_visibility="collapsed")
                # if(f_name != ""):
                #     # create change file name
                #     with  change_f_name_col:                        
                #         change_f_name = st.button ("Change file name", on_click=enable_file_name)

                #     f_name = f_name + ".csv"
                #     df.to_csv(f_name, index=False)
                #     uploaded_file = f_name 
                    # remove temp files
                    # os.remove("temp.csv"); 
                    # os.remove("temp.csv_Course_Overview.html"); os.remove("temp.csv_requirements.html"); 
                    # os.remove("temp.csv_Summative_assessment_only.html");os.remove("temp.csv_All_ERs.html"); 
                    # os.remove("temp.csv_vertical_requirements.html")

              
                    
                    
                    
    if (uploaded_file is not None):
        # store file in a dataframe 
        dataframe = pd.read_csv(uploaded_file)

        #get file labe:
        if(type(uploaded_file) == str):
            label = uploaded_file 
        else:
            label = uploaded_file.name
        
        # get the csv file as array
        csvRows = []
        with open(label, encoding='utf_8_sig') as csvfile:
            reader = csv.reader(csvfile) # change contents to floats
            for row in reader: # each row is a list
                csvRows.append(row)
        view = views.Views(dataframe, csvRows)
        try:
            select_node_edit = dataset.get_selected_node()
        except:
            select_node_edit = None
        try:
            select_node_edit2 = dataset.get_selected_node2()
        except:
            select_node_edit2 = None
        
        view.set_select_edit_node(select_node_edit, select_node_edit2)
         #download csv file
        with col3:
            d_btn = st.button("Download CSV File")

        # another container for the html components of the actual visualization
       

        # get the backgrounf color of the canvas. if true creates customization menu and if false set the colors to the pumpkin color palette
        custom_menu = _Customization_menu(True, view)
        bg = custom_menu.create_menu()
        physics = custom_menu.physics
        font_color = "black" if bg == "white" else "white"
        reset_clicked = custom_menu.resetButton
        atomic_min_size = custom_menu.atomic_min_size
        atomic_max_size = custom_menu.atomic_max_size
        start_end_size = custom_menu.start_end_size
        ier_size = custom_menu.iER_size
        aer_size = custom_menu.aER_size
        rer_size = custom_menu.rER_size
        view.set_atomic_size_limit(atomic_max_size, atomic_min_size, start_end_size, ier_size, aer_size, rer_size)
        
        __create_html_pages(label, view, bg, font_color, view1, physics, d_btn); 

         # adding html file to the container based on the selction made by user
        with container_html:
            if option == view1:
                HtmlFile = open(label+"_Summative_assessment_only.html", 'r', encoding='utf-8')
                source_code = HtmlFile.read() 
                st.components.v1.html(source_code, height=820, scrolling=True)
            elif option == view2:
                HtmlFile = open(label+"_Course_Overview.html", 'r', encoding='utf-8')
                source_code = HtmlFile.read() 
                st.components.v1.html(source_code, height=820, scrolling=True)
            elif option == view3:
                HtmlFile = open(label+"_All_ERs.html", 'r', encoding='utf-8')
                source_code = HtmlFile.read() 
                st.components.v1.html(source_code, height=820, scrolling=True)
            elif option == view4:
                HtmlFile = open(label+"_requirements.html", 'r', encoding='utf-8')
                source_code = HtmlFile.read() 
                st.components.v1.html(source_code, height=820, scrolling=True)
            elif option == view5:
                HtmlFile = open(label+"_vertical_requirements.html", 'r', encoding='utf-8')
                source_code = HtmlFile.read() 
                st.components.v1.html(source_code, height=820, scrolling=True)
    # the legend of the menu
        with st.expander("Legend"):
            # the legend is created using `create_legend` method of views.py which creates a temp html file called 
            # index.legend.html
            legend = Legend.Legend()
            colors = view.getColors()
            legend.setColors(colors)
            legend.create_legend(bg, font_color)
            HtmlFile = open("index_Legend.html", 'r', encoding='utf-8')
            source_code = HtmlFile.read() 
            # the Static html file is added to the streamlit using the components
            st.components.v1.html(source_code, height = 300)  
