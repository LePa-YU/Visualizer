import os
import streamlit as st
import pandas as pd
import numpy as np
import time

class validity_checker:
    def __init__(self, file_name):
        self.file_name = file_name; self.num = 0 
        self.df = pd.read_csv(self.file_name )
        self.validity_file_name = self.file_name.replace(".csv", "_validity_report.txt")
        if(not os.path.isfile(self.validity_file_name)): 
            validity_file= open(self.validity_file_name, "w")
            validity_file.close()

    def check_validity(self):
        validity_file= open(self.validity_file_name, "w")
        for i in range(len(self.df.index)):
            node_id = self.df["identifier"][i]
            node_type = self.df["type"][i]
            node_title = self.df["title"][i]
            if node_type != "start" and node_type != "end":
                if node_type == "rER": 
                    assesses = self.df["assesses"][i]
                    if pd.isna(self.df.loc[i,'assesses']):
                        self.num = self.num + 1
                        validity_file.write(str(self.num)+". Node: " + str(node_title)+ " | ID: "+ str(node_id)+ " of type: " + str(node_type) + " Must assess an aER! \n")
                elif node_type == "iER" or node_type == "aER": 
                    # ca = self.df["comesAfter"][i]
                    if pd.isna(self.df.loc[i,'comesAfter']):
                        self.num = self.num + 1
                        validity_file.write(str(self.num)+". Node: " + str(node_title)+ " | ID: "+ str(node_id)+ " of type: " + str(node_type) + " Must comes after an aER or iER! \n")
                else: # node is atomic --> isPartOF
                    if pd.isna(self.df.loc[i,'isPartOf']):
                        self.num = self.num + 1
                        validity_file.write(str(self.num)+". Node: " + str(node_title)+ " | ID: "+ str(node_id)+ " of type: " + str(node_type) + " Must be part of a composite ER! \n")
        validity_file.close()
    
                
    def clear_report(self):
        open(self.validity_file_name, 'w').close()
        self.num = 0