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
        with st.expander("Options"):
            option=st.selectbox('select graph',('whole LePa','view 2', 'view 3'))
            physics=st.checkbox('add physics interactivity?')
        with st.expander("Customization"):
            bg = st.selectbox('select bakground color', ('white', "black"))
        if option == 'whole LePa':
            views.viewAll(uploaded_file, physics, bg)
            HtmlFile = open("viewAll.html", 'r', encoding='utf-8')
            source_code = HtmlFile.read() 
            st.components.v1.html(source_code, height=1080, scrolling=True)
        elif option == 'view 2':
            views.view_2(uploaded_file, physics, bg)
            HtmlFile = open("view2.html", 'r', encoding='utf-8')
            source_code = HtmlFile.read() 
            st.components.v1.html(source_code, height=1080, scrolling=True)
        elif option == 'view 3':
            views.view_3(uploaded_file, physics)
            HtmlFile = open("view3.html", 'r', encoding='utf-8')
            source_code = HtmlFile.read() 
            st.components.v1.html(source_code, height=1080, scrolling=True)
 ###   