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
                dark = st.checkbox("dark theme")
                if(dark):
                    bg = "black"
                else:
                    bg = "white"

                # 7 element color options for different entities, the sencond arg is the initial color based on pumpkin color palete
                col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns(9)
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
                    start_node_color = st.color_picker('start node color', "#36454F")
                with col9:
                    end_node_color = st.color_picker('end node color', "#36454F")
                
            # set colors based on the selection
            self.view.setColors(aER_node_color, rER_node_color, iER_node_color,  general_node_color, assess_edge_color, comesAfter_edge_color, isPartOf_edge_color, start_node_color, end_node_color ) 
        else:
            self.view.setColors("#FF7273", "#FF7273", "#F69159", "#ECD19A", "#FF7273", "#C0CB6B", "#ECD19A", "#36454F", "#36454F")
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
    # get demo file from github in the Dataset repo (main) 
    url = "https://raw.githubusercontent.com/LePa-YU/Datasets/main/FAKE1001/FAKE1001.csv"
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
    #get file labe:
    if(type(uploaded_file) == str):
        label = uploaded_file
    else:
        label = uploaded_file.name
    view = views.Views(dataframe)

    with container: # add items to container
       #Select view menu
        with st.expander("Select View"):
            #  different views to be selected
            view1 = 'View 1: Summative assessment only'
            view2 = 'View 2: Course Overview'
            view3 = 'View 3: All ERs'
            view4 = "View 4: Requirements"
            option=st.selectbox('',(view1, view2, view3, view4))
        
        # get the backgrounf color of the canvas. if true creates customization menu and if false set the colors to the pumpkin color palette
        custom_menu = _Customization_menu(False, view)
        bg = custom_menu.create_menu()
        font_color = "black" if bg == "white" else "white"
    
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

        # another container for the html components of the actual visualization
        container_html = st.container()
        
        # create the temp html files for each views
        view.Summative_assessment_only( bg, font_color, label, view1)
        view.Course_Overview( bg, font_color, label, view3)
        view.All_ERs( bg, font_color, label, view3)
        view.Requirements(bg, font_color, label, view4)
        
         # adding html file to the container based on the selction made by user
        with container_html:
            if option == view1:
                HtmlFile = open("Summative_assessment_only.html", 'r', encoding='utf-8')
                source_code = HtmlFile.read() 
                st.components.v1.html(source_code, height=820, scrolling=True)
            elif option == view2:
                HtmlFile = open("Course_Overview.html", 'r', encoding='utf-8')
                source_code = HtmlFile.read() 
                st.components.v1.html(source_code, height=820, scrolling=True)
            elif option == view3:
                HtmlFile = open("All_ERs.html", 'r', encoding='utf-8')
                source_code = HtmlFile.read() 
                st.components.v1.html(source_code, height=820, scrolling=True)
            elif option == view4:
                HtmlFile = open("requirements.html", 'r', encoding='utf-8')
                source_code = HtmlFile.read() 
                st.components.v1.html(source_code, height=820, scrolling=True)
            

