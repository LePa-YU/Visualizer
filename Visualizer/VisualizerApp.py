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
##############################################################################################
# function to create html pages
def __create_html_pages(label, view, bg, font_color, view1, physics, download_dataset_only):
    view.Summative_assessment_only( bg, font_color, label, view1, physics, download_dataset_only)
    view.Course_Overview( bg, font_color, label, view2, physics, download_dataset_only)
    view.All_ERs( bg, font_color, label, view3, physics, download_dataset_only)
    view.Requirements(bg, font_color, label, view4, physics, download_dataset_only)
    view.vertical_Requirements(bg, font_color, label, view5, physics, download_dataset_only)
##############################################################################################
# function that allows downloading:
# 1. dataset only 
# 2. downloading session (coming soon)
def download_dataset(uploaded_file):
    c_down = False
    dow_container = st.container(); report  = ""
    with dow_container:
        validity_file_name = uploaded_file.replace(".csv", "_validity_report.txt")
        validity = validity_checker.validity_checker(uploaded_file)
        validity.check_validity() 
        report_file = open(validity_file_name, "r")
        report = report_file.read()
        report_file.close()
        myList = report.splitlines()
        
        #    if report == "": st.write("All issues are solved") 
        # if os.path.getsize(validity_file_name) == 0 and report == "":
        dow_options = st.radio("", ("Download Dataset File (.CSV)", "Download Coordinate File (.JSON)"))
        # save_file = st.checkbox("Download CSV File")
        if(dow_options == "Download Dataset File (.CSV)"):
                if os.path.getsize(validity_file_name) != 0 and report != "":
                    validity_report = st.expander("Please fix the following issues:") 
                    with validity_report:
                        for s in myList:
                            if 'The following ERs are missing titles' in s:
                                if st.checkbox("Missing Titles"):
                                    st.write(s)
                            if 'The following ERs are missing type' in s:
                                if st.checkbox("Missing Types"):
                                    st.write(s)
                    
                            if 'The following ERs are missing both description and url' in s:
                                if st.checkbox("Missing Descriptions/URLs"):
                                    st.write(s)
                        
                            if 'The following ERs are missing an Assesses Relationship' in s:
                                if st.checkbox("Missing 'Assesses' Relationship"):
                                    st.write(s)

                            if 'The following ERs are missing a Comes After Relationship' in s:
                                if st.checkbox("Missing 'Comes After' Relationship"):
                                    st.write(s)
                        
                            if 'The following ERs are missing a IsPartOf Relationship' in s:
                                if st.checkbox("Missing 'Is Part Of' Relationship"):
                                    st.write(s)

                    st.warning("Note that there are some issues with the dataset you are about to download. Check the report above.")
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
        else:
            c_down = True
    return c_down
##############################################################################################
# function that removes existing dataset and corresponding html and validity files. 
def reset_dataset(uploaded_file, delete_file_rec):
    if os.path.exists(uploaded_file):
        os.remove(uploaded_file)
        validity_file = uploaded_file.replace(".csv", "_validity_report.txt")
        if os.path.exists(validity_file):
            os.remove(validity_file) 
        cleaning_report = uploaded_file.replace(".csv","_cleaning_report.txt")
        if os.path.exists(cleaning_report):
            os.remove(cleaning_report) 
    if os.path.exists(str(uploaded_file) + "_Course_Overview.html"):    
        os.remove(str(uploaded_file) + "_Course_Overview.html") 
    if os.path.exists(str(uploaded_file) +"_requirements.html"): 
        os.remove(str(uploaded_file) +"_requirements.html") 
    if os.path.exists(str(uploaded_file) + "_Summative_assessment_only.html"):    
        os.remove(str(uploaded_file) + "_Summative_assessment_only.html")
    if os.path.exists(str(uploaded_file) + "_All_ERs.html"):      
        os.remove(str(uploaded_file) + "_All_ERs.html"); 
    if os.path.exists(str(uploaded_file) + "_vertical_requirements.html"):    
        os.remove(str(uploaded_file) + "_vertical_requirements.html"); 
        
    if delete_file_rec:
            if os.path.exists("file_name_record.txt"): 
                os.remove("file_name_record.txt")      
##########################################################################################################
# Start:    
#global variables:
uploaded_file = None # file that contains the csv file used for visualization/ customization
global df # dataframe of the csv file
download_dataset_only = False
# initial settings for the streamlit app:
# the "wide" layout allows the elements to be stretched to the size of the screen 
st.set_page_config(page_title = "LePa Visualizer", layout="wide", initial_sidebar_state="collapsed")
st.title('LePa: Learning Path Project')
# container that contains menus + visualizer --> helps with responsiveness
container = st.container()
with container:
    # link to other dataset
    st.write("[Other datasets](https://github.com/LePa-YU/Datasets)")
    #col1: existing dataset linked to `Dataset` repo
    col1, col2= st.columns(2)
    with col1:
        fake_ds = "FAKE1001"
        ds_2311 = "EECS 2311"
        ds_3461 = "EECS 3461"
        ds_1530 = "EECS 1530"
        ds_4462 = "EECS 4462"
        enter_own = "Custom dataset"
        dataset_options=st.selectbox('',(fake_ds, ds_2311, ds_3461, ds_1530, ds_4462, enter_own), label_visibility="collapsed")
    #col2: current views, view 3-5 are same with different layouts
    with col2:
        view1 = 'View 1: Summative assessment only'
        view2 = 'View 2: Course Overview'
        view3 = 'View 3: All ERs'
        view4 = "View 4: Requirements"
        view5 = "View 5: Requirements - Vertical"
        option=st.selectbox('',(view1, view2, view3, view4, view5), label_visibility="collapsed")
    #create layout for custom dataset --> change the screen real state for better viewing
    # basically giving different size container to hold the static html
    if dataset_options == enter_own:
        upload_col, edit_col = st.columns([3.5, 4.5])
        with edit_col:
            container_html = st.container()
    else:    
        container_html = st.container()
    # ToDo: this section could use some refactoring
    # getting data for the existing datasets from Dataset repo's main branch:
    # Fake1001.csv
    if dataset_options == fake_ds:
        url = "https://raw.githubusercontent.com/LePa-YU/Datasets/main/FAKE1001/FAKE1001.csv"
        res = requests.get(url, allow_redirects=True)
        #if record of this file exists in the system (duplicate names)--> remove it
        if os.path.exists("file_name_record.txt"):
            with open("file_name_record.txt","r") as f:
                pre_file = (f.read())
                reset_dataset(pre_file, False) 
        # add this dataset to the record
        with open("file_name_record.txt","w") as f:
            f.write('FAKE1001.csv')
        # create a temp csv file (added to .gitignore) and copy csv data into this file
        with open('FAKE1001.csv','wb') as file:
            file.write(res.content)
        uploaded_file = "FAKE1001.csv"
    # EECS 2311
    elif dataset_options == ds_2311:
        url = "https://raw.githubusercontent.com/LePa-YU/Datasets/main/EECS2311/2311_dataset_overview.csv"
        res = requests.get(url, allow_redirects=True)
        if os.path.exists("file_name_record.txt"):
            with open("file_name_record.txt","r") as f:
                pre_file = (f.read())
                reset_dataset(pre_file, False) 
        with open("file_name_record.txt","w") as f:
            f.write("2311_dataset_overview.csv")
        with open('2311_dataset_overview.csv','wb') as file:
            file.write(res.content)
        uploaded_file = "2311_dataset_overview.csv"
    # EECS3461
    elif dataset_options == ds_3461:
        url = "https://raw.githubusercontent.com/LePa-YU/Datasets/main/EECS3461/3461_dataset_overview.csv"
        res = requests.get(url, allow_redirects=True)
        if os.path.exists("file_name_record.txt"):
            with open("file_name_record.txt","r") as f:
                pre_file = (f.read())
                reset_dataset(pre_file, False) 
        with open("file_name_record.txt","w") as f:
            f.write("3461_dataset_overview.csv")
        with open('3461_dataset_overview.csv','wb') as file:
            file.write(res.content)
        uploaded_file = "3461_dataset_overview.csv"
    #EECS 1530
    elif dataset_options == ds_1530:
        url = "https://raw.githubusercontent.com/LePa-YU/Datasets/main/EECS1530/1530_dataset_overview.csv"
        res = requests.get(url, allow_redirects=True)
        if os.path.exists("file_name_record.txt"):
            with open("file_name_record.txt","r") as f:
                pre_file = (f.read())
                reset_dataset(pre_file, False) 
        with open("file_name_record.txt","w") as f:
            f.write("1530_dataset_overview.csv")
        with open('1530_dataset_overview.csv','wb') as file:
            file.write(res.content)
        uploaded_file = "1530_dataset_overview.csv"
    # EECS4462
    elif dataset_options == ds_4462: 
        url = "https://raw.githubusercontent.com/LePa-YU/Datasets/main/EECS4462/4462_dataset_overview.csv"
        res = requests.get(url, allow_redirects=True)
        if os.path.exists("file_name_record.txt"):
            with open("file_name_record.txt","r") as f:
                pre_file = (f.read())
                reset_dataset(pre_file, False) 
        with open("file_name_record.txt","w") as f:
            f.write("4462_dataset_overview.csv")
        with open('4462_dataset_overview.csv','wb') as file:
            file.write(res.content)
        uploaded_file = "4462_dataset_overview.csv"
    # custom dataset
    elif dataset_options == enter_own:
        with upload_col:
            dataset = None
             # to write on the file browser itself on streamlit
            st.markdown(
                        """
                        <style>
                            .css-9ycgxx::before {
                                content: "Load dataset, ";
                            }
                        <style>
                        """
                , unsafe_allow_html=True)
            # file browser    
            u_file = st.file_uploader(label="Load Dataset:", type="csv", help = "Load your dataset  here", label_visibility= "hidden")
            # user has entered a file
            if u_file is not None:    
                # check for file record if it exists remove the previous open files
                if os.path.exists("file_name_record.txt"):
                    with open("file_name_record.txt","r") as f:
                        pre_file = (f.read())
                        if pre_file != u_file.name:
                            reset_dataset(pre_file, False)  

                with open("file_name_record.txt","w") as f:
                    f.write(u_file.name)
                uploaded_file = u_file.name
                if not os.path.exists(u_file.name):
                    with open(u_file.name,"wb") as f:
                        f.write(u_file.getbuffer())
            # user is starting from scratch
            else:
                f_name = "New Dataset.csv"
                if os.path.exists("file_name_record.txt"):
                    with open("file_name_record.txt","r") as f:
                        pre_file = (f.read())
                        if pre_file != f_name:
                            reset_dataset(pre_file, False)
                with open("file_name_record.txt","w") as f:
                    f.write(f_name)
                uploaded_file = f_name
            # instantiating dataset creator to allow customization of new/ entered dataset
            dataset = datasetCreator.datasetCreator(uploaded_file) 
            
            #cleaning report
            cleaning_file_name = uploaded_file.replace(".csv", "_cleaning_report.txt")
            cleaning_file = open(cleaning_file_name, "r+")            
            clean = cleaning_file.read()
            myList2 = clean.splitlines()

            AR =[]
            RR =[]
            CR = []
            IPR = []

            for x in myList2:
                if 'Removed the assesses relation' in x:
                    AR.append(x)
                if 'Removed the requires relation' in x:
                    RR.append(x)   
                if 'Removed the comesAfter relation' in x:
                    CR.append(x)  
                if 'Removed the isPartOf relation' in x:
                    IPR.append(x)

            if clean != "":
                cleaning_report = st.expander("The following issues have been fixed") 
                with cleaning_report:
                    if st.checkbox("Assesses Relation"):
                        for y in AR:
                            st.write(y) 
                            st.write('\n')

                    if st.checkbox("Requires Relation"):
                        for y in RR:
                            st.write(y) 
                            st.write('\n')

                    if st.checkbox("Comes After Relation"):
                        for y in CR:
                            st.write(y) 
                            st.write('\n')

                    if st.checkbox("Is Part of Relation"):
                        for y in IPR:
                            st.write(y) 
                            st.write('\n')
                    
            cleaning_file.close()
              
            new_df_container = st.container() # container containing the options for editing dataset
            with new_df_container:
                if dataset!=None:
                    st.divider() # creating a line
                    # if the user is uploading a dataset then they remove it by removing it from the file uploader
                    # else a delete option avaiable for them
                    if uploaded_file == "New Dataset.csv":
                        node_option = st.radio("What do you want to do?", ("Add a new ER", "Update a ER", "Modify Relations", "Delete Dataset"), key="node_tab")
                    else:
                        node_option = st.radio("What do you want to do?", ("Add a new ER", "Update a ER", "Modify Relations"), key="node_tab") 
                    if(node_option == "Add a new ER"):
                        dataset.add_node()
                    elif(node_option == "Update a ER"):
                        dataset.edit_node()
                    elif(node_option == "Modify Relations"):
                        dataset.add_relation()
                    elif(node_option == "Delete Dataset"):
                        del_btn = st.button("Delete Dataset?")
                        if del_btn: 
                            if os.path.exists("file_name_record.txt"):
                                with open("file_name_record.txt","r") as f:
                                    pre_file = (f.read())
                                    reset_dataset(pre_file, False)
                            f_name = "New Dataset.csv"
                            with open("file_name_record.txt","w") as f:
                                f.write(f_name)
                            uploaded_file = f_name
                            dataset = datasetCreator.datasetCreator(f_name)  
                    #flag that indicates user want to download the dataset
                    download_dataset_only = download_dataset(uploaded_file)           
    if (uploaded_file is not None):
        # store file in a dataframe  used for views --> Visualization file
        dataframe = pd.read_csv(uploaded_file)

        #get file labe:
        if(type(uploaded_file) == str):
            label = uploaded_file 
        else:
            label = uploaded_file.name
        
        # get the csv file as array -
        csvRows = []
        # with open(label, encoding='utf_8_sig') as csvfile:
        #     reader = csv.reader(csvfile) # change contents to floats
        #     for row in reader: # each row is a list
        #         csvRows.append(row)
        view = views.Views(dataframe, csvRows)
        
        # for the custom dataset we retrive a selected node if they exists
        try:
            select_node_edit = dataset.get_selected_node()
        except:
            select_node_edit = None
        try:
            select_node_edit2 = dataset.get_selected_node2()
        except:
            select_node_edit2 = None
        # pass selected nodes to views so they can be visualized 
        view.set_select_edit_node(select_node_edit, select_node_edit2)

        # Customization menu -- color, size, physics, etc. 
        # get the background color of the canvas. if true creates customization menu and if false set the colors to the pumpkin color palette
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
        
        # create 5 htmls containing different layout of datasets
        # view1 is used for mobile warning when creating the html -- cannot have warning in streamlit
        __create_html_pages(label, view, bg, font_color, view1, physics, download_dataset_only); 

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
            there_is_icon = False
            if option == view4 or option == view5: there_is_icon = True
            # print(there_is_icon)
            legend = Legend.Legend()
            colors = view.getColors()
            legend.setColors(colors)
            legend.create_legend(bg, font_color, there_is_icon)
            HtmlFile = open("index_Legend.html", 'r', encoding='utf-8')
            source_code = HtmlFile.read() 
            # the Static html file is added to the streamlit using the components
            st.components.v1.html(source_code, height = 300)  
