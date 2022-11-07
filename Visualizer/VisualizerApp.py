import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
import views 



#### this file contains code for streamlit deployment

st.title('LePa: Learning Path Project')
cont = st.container
st.sidebar.title('Choose your view')
option=st.sidebar.selectbox('select graph',('whole LePa','view 2', 'view 3'))
physics=st.sidebar.checkbox('add physics interactivity?')
demo = st.checkbox("use demo file")

# physics=st.sidebar.checkbox('add physics interactivity?')
if demo: 
    # get demo file from github
    # url = "https://drive.google.com/file/d/1kWkw57BPSKQ-my37NvHXszcMbuKFw7B0/view?usp=sharing"
    # res = requests.get(url, allow_redirects=True)
    # with open('demo.csv','wb') as file:
    #     file.write(res.content)
    # from google drive
    url="https://drive.google.com/file/d/1kWkw57BPSKQ-my37NvHXszcMbuKFw7B0/view?usp=sharing"
    url='https://drive.google.com/uc?id=' + url.split('/')[-2]
    df = pd.read_csv(url)
    df.to_csv("demo.csv")

    uploaded_file = "demo.csv"

else:
    uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    if option=='whole LePa':
        views.viewAll(uploaded_file, physics)
        HtmlFile = open("viewAll.html", 'r', encoding='utf-8')
        source_code = HtmlFile.read() 
        st.components.v1.html(source_code, height=1500,width=700, scrolling=True)
        # components.html(source_code, height = 900,width=900)

    if option=='view 2':
        views.view_2(uploaded_file)
        HtmlFile = open("view2.html", 'r', encoding='utf-8')
        source_code = HtmlFile.read() 
        st.components.v1.html(source_code, height=1500,width=700, scrolling=True)
