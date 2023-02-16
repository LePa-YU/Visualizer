# required imports
import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import networkx as nx
from pyvis.network import Network
import views 
import requests
import Legend

#### this file contains code for streamlit deployment

# function for customization menu
def __customization_menu(create_customization_menu):
    bg = "white"
    if(create_customization_menu):
        # customization menu --> temporary. comment before releases
        with st.expander("Customization"):
            # Theme options
            
            # background
            bg = ""
            # dark --> boolean -- true then background is set to black and text to white/ fasle then background is set to white and text is set to black
            dark = st.checkbox("dark theme")
            if(dark):
                bg = "black"
            else:
                bg = "white"

            # 7 element color options for different entities, the sencond arg is the initial color based on pumpkin color palete
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
    else:
        views.setColors("#FF7273", "#FF7273", "#F69159", "#ECD19A", "#FF7273", "#C0CB6B", "#ECD19A")
    return bg

#global variables:
global uploaded_file

# initial settings:
    # the "wide" layout allows the elements to be stretched to the size of the screen 
st.set_page_config(page_title = "LePa Visualizer", layout="wide", initial_sidebar_state="collapsed")
st.title('LePa: Learning Path Project')

# demo check box --> boolean if true the demo is displayed 
demo = st.checkbox("Load FAKE1001 dataset or  Load other dataset (default) ")
# link to other dataset
st.write("[Other datasets](https://github.com/LePa-YU/Datasets)")

# if demo is selected
if demo: 
    # get demo file from github in the development branch --> change to one from main branch if necessary
    url = "https://raw.githubusercontent.com/LePa-YU/Visualizer/development/Data/FAKE1001.csv"
    res = requests.get(url, allow_redirects=True)
    # create a temp csv file (added to .gitignore) and copy the material from the link to this file
    with open('FAKE1001.csv','wb') as file:
        file.write(res.content)
    uploaded_file = "FAKE1001.csv"
# otherwise get the file from browser
else:
    # to write on the file browser itself
    st.markdown(
    """
    <style>
        .css-9ycgxx::before {
            content: "Load dataset, ";
        }
    <style>
    """, unsafe_allow_html=True)
    # user enters csv file in the file_uplader with the following properties
    uploaded_file = st.file_uploader(label="Load Dataset:", type="csv", help = "Load your dataset  here", label_visibility= "hidden")

    
# container that contains menus + visualizer --> helps with responsive attribute
container = st.container()

# if a file a selected (demo or user browsed file) then we go through visualization
if uploaded_file is not None:
    # store file in a dataframe 
    dataframe = pd.read_csv(uploaded_file)

    with container: # add items to container
       #Select view menu
        with st.expander("Select View"):
            #  different views to be selected
            view1 = 'View 1: Summative assessment only'
            view2 = 'View 2: Course Overview'
            view3 = 'View 3: All ERs'
            option=st.selectbox('',(view1, view2, view3))
        
        # get the backgrounf color of the canvas. if true creates customization menu and if false set the colors to the pumpkin color palette
        bg = __customization_menu(False)

       # the legend of the menu
        with st.expander("Legend"):
            # the legend is created using `create_legend` method of views.py which creates a temp html file called 
            # index.legend.html
            Legend.setColors("#FF7273", "#FF7273", "#F69159", "#ECD19A", "#FF7273", "#C0CB6B", "#ECD19A")
            Legend.create_Legend()
            HtmlFile = open("index_Legend.html", 'r', encoding='utf-8')
            source_code = HtmlFile.read() 
            # the Static html file is added to the streamlit using the components
            st.components.v1.html(source_code, height = 300)

        # another container for the html components of the actual visualization
        container_html = st.container()

        #get file labe:
        if(type(uploaded_file) == str):
            label = uploaded_file
        else:
            label = uploaded_file.name
        
        # create the temp html files for each views
        views.All_ERs(dataframe, bg, label, view3)
        views.Course_Overview(dataframe, bg, label, view2)
        views.Summative_assessment_only(dataframe, bg, label, view1)
        
        # adding html file to the container based on the selction made by user
        with container_html:
            if option == view3:
                HtmlFile = open("All_ERs.html", 'r', encoding='utf-8')
                source_code = HtmlFile.read() 
                st.components.v1.html(source_code, height=820, scrolling=True)
            elif option == view2:
                HtmlFile = open("Course_Overview.html", 'r', encoding='utf-8')
                source_code = HtmlFile.read() 
                st.components.v1.html(source_code, height=820, scrolling=True)
            elif option == view1:
                HtmlFile = open("Summative_assessment_only.html", 'r', encoding='utf-8')
                source_code = HtmlFile.read() 
                st.components.v1.html(source_code, height=820, scrolling=True)
        
