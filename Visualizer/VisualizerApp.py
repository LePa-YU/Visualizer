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

#### this file contains code for streamlit deployment
class _Customization_menu:
    def __init__(self, create_customization_menu, view):
        self.create_customization_menu = create_customization_menu
        self.view = view
    def create_menu(self):
        bg = "white"
        if(self.create_customization_menu):
            # customization menu --> temporary. comment before releases
            with st.expander("Customization"):
                # Theme options
                # dark --> boolean -- true then background is set to black and text to white/ fasle then background is set to white and text is set to black
                st.subheader("Options:")
                colbg, colphys = st.columns([1, 8])
                with colbg:
                    dark = st.checkbox("dark theme")
                    if(dark):
                        bg = "black"
                    else:
                        bg = "white"
                with colphys:
                    self.physics = st.checkbox("physics")

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

def __create_html_pages(label, view, bg, font_color, view1, physics):
     # create the temp html files for each views
        # add if-else statemet --> create html if it does not exsits
        path = "./html_temp/"+label+"_Summative_assessment_only.html"
        check_file = os.path.isfile(path)
        if(check_file == False):
            view.Summative_assessment_only( bg, font_color, label, view1, physics)
        
        path = label+"_Course_Overview.html"
        check_file = os.path.isfile(path)
        if(check_file == False):
            view.Course_Overview( bg, font_color, label, view2, physics)
        
        path = label+"_All_ERs.html"
        check_file = os.path.isfile(path)
        if(check_file == False):
            view.All_ERs( bg, font_color, label, view3, physics)
        
        path = label+"_requirements.html"
        check_file = os.path.isfile(path)
        if(check_file == False):
            view.Requirements(bg, font_color, label, view4, physics)

#global variables:
global uploaded_file

# initial settings:
    # the "wide" layout allows the elements to be stretched to the size of the screen 
st.set_page_config(page_title = "LePa Visualizer", layout="wide", initial_sidebar_state="collapsed")
st.title('LePa: Learning Path Project')

# container that contains menus + visualizer --> helps with responsive attribute
container = st.container()

with container:
    # link to other dataset
    st.write("[Other datasets](https://github.com/LePa-YU/Datasets)")
    
    col1, col2= st.columns(2)
    with col1:
        fake_ds = "FAKE1001"
        ds_2311 = "EECS 2311"
        ds_3461 = "EECS 3461"
        ds_1530 = "EECS 1530"
        ds_4462 = "EECS 4462"
        enter_own = "Enter your own data"
        dataset_options=st.selectbox('',(fake_ds, ds_2311, ds_3461, ds_1530, ds_4462, enter_own))
    with col2:
        view1 = 'View 1: Summative assessment only'
        view2 = 'View 2: Course Overview'
        view3 = 'View 3: All ERs'
        view4 = "View 4: Requirements"
        option=st.selectbox('',(view1, view2, view3, view4))
    
    if dataset_options == fake_ds:
        # get demo file from github in the Dataset repo (main) 
        url = "https://raw.githubusercontent.com/LePa-YU/Datasets/main/FAKE1001/FAKE1001.csv"
        res = requests.get(url, allow_redirects=True)
        # create a temp csv file (added to .gitignore) and copy the material from the link to this file
        with open('./csv_temp/FAKE1001.csv','wb') as file:
            file.write(res.content)
            uploaded_file = "./csv_temp/FAKE1001.csv"
    elif dataset_options == ds_2311:
        # get EECS 2311 file from github in the Dataset repo (main) 
        url = "https://raw.githubusercontent.com/LePa-YU/Datasets/main/EECS2311/2311_dataset_overview.csv"
        res = requests.get(url, allow_redirects=True)
        # create a temp csv file (added to .gitignore) and copy the material from the link to this file
        with open('./csv_temp/2311_dataset_overview.csv','wb') as file:
            file.write(res.content)
            uploaded_file = "./csv_temp/2311_dataset_overview.csv"
    elif dataset_options == ds_3461:
        # get EECS 3461 file from github in the Dataset repo (main) 
        url = "https://raw.githubusercontent.com/LePa-YU/Datasets/main/EECS3461/3461_dataset_overview.csv"
        res = requests.get(url, allow_redirects=True)
        # create a temp csv file (added to .gitignore) and copy the material from the link to this file
        with open('./csv_temp/3461_dataset_overview.csv','wb') as file:
            file.write(res.content)
            uploaded_file = "./csv_temp/3461_dataset_overview.csv"
    elif dataset_options == ds_1530:
        # get EECS 1530 file from github in the Dataset repo (main) 
        url = "https://raw.githubusercontent.com/LePa-YU/Datasets/main/EECS1530/1530_dataset_overview.csv"
        res = requests.get(url, allow_redirects=True)
        # create a temp csv file (added to .gitignore) and copy the material from the link to this file
        with open('./csv_temp/1530_dataset_overview.csv','wb') as file:
            file.write(res.content)
            uploaded_file = "./csv_temp/1530_dataset_overview.csv"
    elif dataset_options == ds_4462:
        # get EECS 4462 file from github in the Dataset repo (main) 
        url = "https://raw.githubusercontent.com/LePa-YU/Datasets/main/EECS4462/4462_dataset_overview.csv"
        res = requests.get(url, allow_redirects=True)
        # create a temp csv file (added to .gitignore) and copy the material from the link to this file
        with open('./csv_temp/4462_dataset_overview.csv','wb') as file:
            file.write(res.content)
            uploaded_file = "./csv_temp/4462_dataset_overview.csv"
    elif dataset_options == enter_own:
        # to write on the file browser itself
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
        uploaded_file = st.file_uploader(label="Load Dataset:", type="csv", help = "Load your dataset  here", label_visibility= "hidden")

    
    
    if uploaded_file is not None:
        # store file in a dataframe 
        dataframe = pd.read_csv(uploaded_file)
        #get file labe:
        if(type(uploaded_file) == str):
            label = uploaded_file.split("csv_temp/",1)[1]
        else:
            label = uploaded_file.name
        
        view = views.Views(dataframe)

        # another container for the html components of the actual visualization
        container_html = st.container()

        # get the backgrounf color of the canvas. if true creates customization menu and if false set the colors to the pumpkin color palette
        custom_menu = _Customization_menu(True, view)
        bg = custom_menu.create_menu()
        physics = custom_menu.physics
        font_color = "black" if bg == "white" else "white"
        
        __create_html_pages(label, view, bg, font_color, view1, physics); 

         # adding html file to the container based on the selction made by user
        with container_html:
            if option == view1:
                HtmlFile = open("./html_temp/"+label+"_Summative_assessment_only.html", 'r', encoding='utf-8')
                source_code = HtmlFile.read() 
                st.components.v1.html(source_code, height=820, scrolling=True)
            elif option == view2:
                HtmlFile = open("./html_temp/"+label+"_Course_Overview.html", 'r', encoding='utf-8')
                source_code = HtmlFile.read() 
                st.components.v1.html(source_code, height=820, scrolling=True)
            elif option == view3:
                HtmlFile = open("./html_temp/"+label+"_All_ERs.html", 'r', encoding='utf-8')
                source_code = HtmlFile.read() 
                st.components.v1.html(source_code, height=820, scrolling=True)
            elif option == view4:
                HtmlFile = open("./html_temp/"+label+"_requirements.html", 'r', encoding='utf-8')
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
