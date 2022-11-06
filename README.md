# Visualizer
A web based tool to represent the AIR model of LePa project

## Description
web based tool created using python and streamlit library to visualize the AIR model from Learning Path Project
## Getting started

### Dependencies
the dependencies can be found in Visualizer/requirements.txt. Here is the list of dependencies:
```
matplotlib==3.6.1
networkx==2.8.7
pandas==1.5.0
pyvis==0.3.0
streamlit==1.13.0

```
the python used for this project is `Python 3.10.7`
### Using Visualizer

#### 1. Web based (recommended)
1. The visualizer tool is hosted on the streamlit cloud which can be accessed through the link 
<a href="https://elmiraon-lepa-visualizernewversionvisualizerapp-elmira-v-wnvo25.streamlit.app/" target="_blank">here</a>. 

![visualizer on streamlit cloud](https://github.com/LePa-YU/Visualizer/blob/main/images/appDemo1.JPG)

2. Browse for csv file representing the learning path or demo check box to visualize your learning path. you can also find the demo data @ `Data/demo.csv`

![visualizer on streamlit cloud](https://github.com/LePa-YU/Visualizer/blob/main/images/appDemo2.jpg)

- using demo result in following graph:

![visualizer demo on streamlit cloud](https://github.com/LePa-YU/Visualizer/blob/main/images/appDemo3.jpg)

3. You can use the menu on left hand to visualize different views of the same dataset:

![visualizer on streamlit cloud](https://github.com/LePa-YU/Visualizer/blob/main/images/appDemo4.jpg)



#### 2. Using VS code
You can also pull the project on VS code (or any other platform that work with python), then follow the steps below:

1. run Visualizer/views.py by running script `python Visualizer\views.py` in terminal (the command might be different based on the platform and python version you have installed) to make sure its error free. 
2. run Visualizer/VisualizerApp.py in the same manner as in step 1. 
3. run script `streamlit run Visualizer\VisualizerApp.py`in terminal. This will open the streamlit application in the web where you can use the same data as web based to use the application. 

### Version history
- v 01: initial release

### License