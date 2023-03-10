# Visualizer
A web based tool to represent the AIR model of LePa project

## Description
web based tool created using python and streamlit library to visualize the AIR model from Learning Path Project
## Getting started

### Dependencies
the dependencies can be found in Visualizer/requirements.txt. Here is the list of dependencies:
```
networkx==2.8.7
pandas==1.5.0
pyvis==0.3.0
requests==2.28.1
streamlit==1.13.0

```
the python used for this project is `Python 3.10.7`
### Using Visualizer


#### 1. Web based (recommended)
1. The visualizer tool is hosted on the streamlit cloud which can be accessed through the link 
<a href="https://lepa-visualizer-development.streamlit.app/" target="_blank">here</a>.  

![visualizer on streamlit cloud](https://github.com/LePa-YU/Visualizer/blob/a330661f7664f7dd617e8481dd4d012a415f538b/images/appDemo1.JPG)

2. Browse for csv file representing the learning path. You can also visualize a demo learning path by checking `load FAKE1001 dataset or other datasets`. The demo csv file can be found @ `Data/demo.csv`. Additionally the link to "other datasets" is provided for ease of access

![visualizer on streamlit cloud](https://github.com/LePa-YU/Visualizer/blob/a330661f7664f7dd617e8481dd4d012a415f538b/images/appDemo2.jpg)

- using demo result in following graph:

![visualizer demo on streamlit cloud](https://github.com/LePa-YU/Visualizer/blob/a330661f7664f7dd617e8481dd4d012a415f538b/images/appDemo3.jpg)

3. You can use the `Select view` menu to access different views of the same dataset

![visualizer on streamlit cloud](https://github.com/LePa-YU/Visualizer/blob/a330661f7664f7dd617e8481dd4d012a415f538b/images/appDemo4.jpg)

- Additionally the `Legend` contains a legend to the graph
- the temporary customization menu allows to experiment with different  colors for entities in both light and dark mode



#### 2. Using VS code
You can also pull the project on VS code (or any other platform that work with python), then follow the steps below:

1. run Visualizer/views.py by running script `python Visualizer\views.py` in terminal (the command might be different based on the platform and python version you have installed) to make sure its error free. 
2. run Visualizer/VisualizerApp.py in the same manner as in step 1. 
3. run script `streamlit run Visualizer\VisualizerApp.py`in terminal. This will open the streamlit application in the web where you can use the same data as web based to use the application. 

## Glossary of Terms, Nomenclature

**dataset**: refers to a csv file containing elements, one per row.  The list of attributes per row adheres to schema <<INSERT SCHEMA IDENTIFIER>>

**layout**: refers to a particular spatial arrangement of the visualization elements (nodes, edges).  Not to be confused with **view**.

**view**: refers to a particular presentation of the underlying data model, in terms of the subset of data displayed and how the data is represented (e.g., the use of different types of node shapes and colours to correspond to different data attributes).
 

### Version history
- v 01: initial release
- V 02: change in layout, additional views and relationships, and specific color palate
- V 03: DJ1

### License
