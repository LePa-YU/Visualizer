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
            if pd.isna(self.df.loc[i,'title']) or node_title=="Missing Title":
                self.num = self.num + 1
                self.df["title"][i] = "Missing Title"
                self.df.to_csv(self.file_name, index=False)
                validity_file.write(str(self.num)+". ER is missing title  | ID: "+ str(node_id) + "| Please delete or add title to node tagged as `Missing Title` using `Update a ER` option\n")
            elif pd.isna(self.df.loc[i,'type']):
                self.num = self.num + 1
                validity_file.write(str(self.num)+". ER `"+ str(node_title) +"` is missing type  | ID: "+ str(node_id) + "| Please delete or add type to this ERs using `Update a ER` option\n")
            elif pd.isna(self.df.loc[i,'description']) and pd.isna(self.df.loc[i,'url']):
                self.num = self.num + 1
                validity_file.write(str(self.num)+". ER `"+ str(node_title) +"` is missing both description and url  | ID: "+ str(node_id) + "| Please delete this ER or update one of these fields using `Update a ER` option\n")
            else:
                if node_type != "start" and node_type != "end":
                    if node_type == "rER": 
                        assesses = self.df["assesses"][i]
                        if pd.isna(self.df.loc[i,'assesses']):
                            self.num = self.num + 1
                            validity_file.write(str(self.num)+". ER: '" + str(node_title)+ "' | ID: "+ str(node_id)+ "| type: " + str(node_type) + "| Must assess an aER! Please create an `assesses` relation using `Modify Relation`\n")
                    elif node_type == "iER" or node_type == "aER": 
                        # ca = self.df["comesAfter"][i]
                        if pd.isna(self.df.loc[i,'comesAfter']):
                            self.num = self.num + 1
                            validity_file.write(str(self.num)+". ER: `" + str(node_title)+ "` | ID: "+ str(node_id)+ "| type: " + str(node_type) + "|  Must comes after an aER or iER! Please create an `comes After` relation using `Modify Relation`\n")
                    else: # node is atomic --> isPartOF
                        if pd.isna(self.df.loc[i,'isPartOf']):
                            self.num = self.num + 1
                            validity_file.write(str(self.num)+". ER: `" + str(node_title)+ "` | ID: "+ str(node_id)+ "| type: " + str(node_type) + "|  Must be part of a composite ER! Please create an `is Part of` relation using `Modify Relation`\n")
        validity_checker.__check_comesAfter_validity(self, validity_file)
        validity_file.close()
    
    def __check_comesAfter_validity(self, report_file):
        # all aER, iER, end must have ca field --> list must be a set
        # aER, iER missing comesAfter is already being validates -- this function validates the existing 
        # one so there is no duplicate referrals
        all_ca_field = []; 
        for i in range(len(self.df.index)):
            try: ca = int(self.df["comesAfter"][i])
            except: ca = None
            if ca != None: all_ca_field.append(ca)
        if len(all_ca_field) != len(set(all_ca_field)):
            # find duplicates
            duplicateList = []; uniqueList = []
            for ca in all_ca_field:
                if ca not in uniqueList:
                    uniqueList.append(ca)
                elif ca not in duplicateList:
                    duplicateList.append(ca)
            # for each duplicate find the nodes they are referring to 
            for dup in duplicateList:
                node_referred = []
                for i in range(len(self.df.index)):
                    try: ca = int(self.df["comesAfter"][i])
                    except: ca = None
                    if (ca == dup):
                        title = self.df["title"][i]
                        n_id = self.df["identifier"][i]
                        n_type = self.df["type"][i]
                        res = {"id": n_id, "title": title, "type": n_type}
                        node_referred.append(res)
                problematic_nodes = ""
                for node in node_referred:
                    problematic_nodes = problematic_nodes + "|" +str(node["title"])+", ID: "+str(node["id"]) + ", type: " + str(node["type"])
                for i in range(len(self.df.index)):
                    try: n_id = int(self.df["identifier"][i])
                    except: n_id = None
                    if (n_id == dup):
                        title = self.df["title"][i]
                        node_type = self.df["type"][i]
                        self.num = self.num + 1
                        report_file.write(str(self.num)+". Multiple ERs come after `" + str(title)+ "` | ID: "+ str(n_id)+ "| type: " + str(node_type) + ": "+problematic_nodes +"| Please fix some of these relation by removing node in `update a node` or updating comesAFter relation in `modify relation` option!\n")
                        break
            # print duplicate + referred node in report
            # print(duplicateList)


    def clear_report(self):
        open(self.validity_file_name, 'w').close()
        self.num = 0