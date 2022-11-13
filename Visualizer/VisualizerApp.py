import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
import views 
import requests



#### this file contains code for streamlit deployment

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
    uploaded_file = st.file_uploader("Choose a file")

# container that contains menus + visualizer
container = st.container()
if uploaded_file is not None: # if a file a selected then we go through visualization
    with container: # add items to container
       #options menu
        with st.expander("Options"):
            option=st.selectbox('select graph',('whole LePa','AIR view', 'view 3'))
            physics=st.checkbox('add physics interactivity?')
        # customization menu
        with st.expander("Customization"):
            bg = st.selectbox('select bakground color', ('white', "black"))
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
        views.setColors(aER_node_color, rER_node_color, iER_node_color, general_node_color, assess_edge_color, requires_edge_color, isPartOf_edge_color)
        if option == 'whole LePa':
            views.viewAll(uploaded_file, physics, bg)
            HtmlFile = open("viewAll.html", 'r', encoding='utf-8')
            source_code = HtmlFile.read() 
            st.components.v1.html(source_code, height=1080, scrolling=True)
        elif option == 'AIR view':
            views.AIR_view(uploaded_file, physics, bg)
            HtmlFile = open("AIR_view.html", 'r', encoding='utf-8')
            source_code = HtmlFile.read() 
            st.components.v1.html(source_code, height=1080, scrolling=True)
        elif option == 'view 3':
            views.view_3(uploaded_file, physics)
            HtmlFile = open("view3.html", 'r', encoding='utf-8')
            source_code = HtmlFile.read() 
            st.components.v1.html(source_code, height=1080, scrolling=True)
 ###   