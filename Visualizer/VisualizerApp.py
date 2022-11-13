import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
import views 
import requests

#### this file contains code for streamlit deployment

#global variables:
global uploaded_file

# initial settings
st.set_page_config(page_title = "LePa Visualizer", layout="wide", initial_sidebar_state="collapsed")
st.title('LePa: Learning Path Project')

# demo check box --> boolean
demo = st.checkbox("use demo file")
if demo: 
    # get demo file from github
    url = "https://raw.githubusercontent.com/LePa-YU/Visualizer/main/Data/demo.csv"
    res = requests.get(url, allow_redirects=True)
    with open('demo.csv','wb') as file:
        file.write(res.content)
    uploaded_file = "demo.csv"
else:
    # user enters csv file
    uploaded_file = st.file_uploader(label="Enter your csv file", type="csv")
    
# container that contains menus + visualizer --> helps with responsive attribute
container = st.container()

# if a file a selected then we go through visualization
if uploaded_file is not None: 
    # store file in a dataframe
    dataframe = pd.read_csv(uploaded_file)
    # set data based on dataframe
    views.setData(dataframe)
    views.get_Id_Rows(dataframe)

    with container: # add items to container
       #options menu
        with st.expander("Options"):
            #  different views
            option=st.selectbox('select graph',('whole LePa','AIR view', 'view 3'))
            # adding physics interactivity
            physics=st.checkbox('add physics interactivity?')
        # customization menu
        with st.expander("Customization"):
            # background options
            bg = st.selectbox('select bakground color', ('white', "black"))
            # 7 element color options
            col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
            with col1:
                aER_node_color = st.color_picker('Pick aER node color', "#FF7273")
            with col2:
                rER_node_color = st.color_picker('Pick rER node color', "#FF7273")
            with col3:
                iER_node_color = st.color_picker('Pick iER node color', "#F69159")
            with col4:
                general_node_color = st.color_picker('Pick general node color', "#ECD19A")
            with col5:
                assess_edge_color = st.color_picker('Pick assess edge color', "#FF7273")
            with col6:
                requires_edge_color = st.color_picker('Pick requires edge color', "#C0CB6B")
            with col7:
                isPartOf_edge_color = st.color_picker('Pick isPartOf edge color', "#ECD19A")
        # set colors based on the selection
        views.setColors(aER_node_color, rER_node_color, iER_node_color, general_node_color, assess_edge_color, requires_edge_color, isPartOf_edge_color)
        
        # set views bassed on view options
        if option == 'whole LePa':
            views.viewAll(physics, bg)
            HtmlFile = open("view.html", 'r', encoding='utf-8')
            source_code = HtmlFile.read() 
            st.components.v1.html(source_code, height=1080, scrolling=True)
        elif option == 'AIR view':
            views.AIR_view(physics, bg)
            HtmlFile = open("view.html", 'r', encoding='utf-8')
            source_code = HtmlFile.read() 
            st.components.v1.html(source_code, height=1080, scrolling=True)
        elif option == 'view 3':
            views.view_3(physics, bg)
            HtmlFile = open("view.html", 'r', encoding='utf-8')
            source_code = HtmlFile.read() 
            st.components.v1.html(source_code, height=1080, scrolling=True)
 ###   