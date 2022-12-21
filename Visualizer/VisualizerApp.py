import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import networkx as nx
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
# demo = st.checkbox("Load FAKE1001 dataset")
# st.write("check out this [link]()")
demo = st.checkbox("Load FAKE1001 dataset or  Load other dataset (default) ")
st.write("[Other datasets](https://github.com/LePa-YU/Datasets)")
if demo: 
    # get demo file from github
    url = "https://raw.githubusercontent.com/LePa-YU/Visualizer/development/Data/FAKE1001.csv"
    res = requests.get(url, allow_redirects=True)
    with open('FAKE1001.csv','wb') as file:
        file.write(res.content)
    uploaded_file = "FAKE1001.csv"
else:
    st.markdown(
    """
    <style>
        .css-9ycgxx::before {
            content: "Load dataset, ";
        }
    <style>
    """, unsafe_allow_html=True)
    # user enters csv file
    uploaded_file = st.file_uploader(label="Load Dataset:", type="csv", help = "Load your dataset  here", label_visibility= "hidden")

    
# container that contains menus + visualizer --> helps with responsive attribute
container = st.container()

# if a file a selected then we go through visualization
if uploaded_file is not None: 
    # store file in a dataframe
    dataframe = pd.read_csv(uploaded_file)
    # set data based on dataframe
    # views.setData(dataframe)

    with container: # add items to container
       #options menu
        with st.expander("Select View"):
            #  different views
            option=st.selectbox('',('View 1: Summative assessment only','View 2: Course Overview','View 3: All ERs'))
        
        # # customization menu
        with st.expander("Customization"):
            # Theme options
            bg = ""
            dark = st.checkbox("dark theme")
            if(dark):
                bg = "black"
            else:
                bg = "white"
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
                requires_edge_color = st.color_picker('Pick comes_after edge color', "#C0CB6B")
            with col7:
                isPartOf_edge_color = st.color_picker('Pick isPartOf edge color', "#ECD19A")
            
        # set colors based on the selection
        views.setColors(aER_node_color, rER_node_color, iER_node_color,  general_node_color, assess_edge_color, requires_edge_color, isPartOf_edge_color  )
        # views.setColors("#FF7273", "#FF7273", "#F69159", "#ECD19A", "#FF7273", "#C0CB6B", "#ECD19A")

        with st.expander("Legend"):
            views.create_Legend()
            HtmlFile = open("index_Legend.html", 'r', encoding='utf-8')
            source_code = HtmlFile.read() 
            st.components.v1.html(source_code, height = 300)

        container_html = st.container()
        # set views bassed on view options
        views.All_ERs(dataframe, bg)
        views.Course_Overview(dataframe, bg)
        views.Summative_assessment_only(dataframe, bg)
        
        with container_html:
            if option == 'View 3: All ERs':
                HtmlFile = open("All_ERs.html", 'r', encoding='utf-8')
                source_code = HtmlFile.read() 
                st.components.v1.html(source_code, height=820, scrolling=True)
            elif option == 'View 2: Course Overview':
                HtmlFile = open("Course_Overview.html", 'r', encoding='utf-8')
                source_code = HtmlFile.read() 
                st.components.v1.html(source_code, height=820, scrolling=True)
            elif option == 'View 1: Summative assessment only':
                HtmlFile = open("Summative_assessment_only.html", 'r', encoding='utf-8')
                source_code = HtmlFile.read() 
                st.components.v1.html(source_code, height=820, scrolling=True)
        
 ###   