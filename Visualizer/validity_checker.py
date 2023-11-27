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
        missingTitle = []
        missingType = []
        missingTypeTitle = []
        missingDes = []
        missingDesTitle =[]
        missingAssesses = []
        missingAssessesTitle = []
        missingAssessType = []
        missingComesAfter =[]
        missingCATitle = []
        missingCAType = []
        missingIsPartOf =[]
        missingIPTitle =[]
        missingIPType =[]
        
        for i in range(len(self.df.index)):

            node_id = self.df["identifier"][i]
            node_type = self.df["type"][i]
            node_title = self.df["title"][i]


            if pd.isna(self.df.loc[i,'title']) or node_title=="Missing Title":
                missingTitle.append(node_id)
                self.df["title"][i] = "Missing Title"
           
            if pd.isna(self.df.loc[i,'type']):
                missingType.append(node_id)
                missingTypeTitle.append(node_title)


            if pd.isna(self.df.loc[i,'description']) and pd.isna(self.df.loc[i,'url']):
                missingDes.append(node_id)
                missingDesTitle.append(node_title)

            else:
                if node_type != "start" and node_type != "end":
                    if node_type == "rER": 
                        assesses = self.df["assesses"][i]
                        if pd.isna(self.df.loc[i,'assesses']):
                            missingAssesses.append(node_id)
                            missingAssessesTitle.append(node_title)
                            missingAssessType.append(node_type)

                    elif node_type == "iER" or node_type == "aER": 
                        # ca = self.df["comesAfter"][i]
                        if pd.isna(self.df.loc[i,'comesAfter']):
                            missingComesAfter.append(node_id)
                            missingCAType.append(node_type)
                            missingCATitle.append(node_title)

                    else: # node is atomic --> isPartOF
                        if pd.isna(self.df.loc[i,'isPartOf']):
                            missingIsPartOf.append(node_id)
                            missingIPTitle.append(node_title)
                            missingIPType.append(node_type)

        missingTitleString = ','.join(map(str, missingTitle))

        if(len(missingTitle) != 0):
            self.num = self.num + 1
            self.df.to_csv(self.file_name, index=False)
            validity_file.write(str(self.num)+". The following ERs are missing titles | ID: "+ missingTitleString + "| Please delete or add title to nodes tagged as `Missing Title` using `Update a ER` option")
            validity_file.write("\n")

        if(len(missingType) != 0):
            self.num = self.num + 1
            validity_file.write(str(self.num)+". The following ERs are missing type: ")
            for i in range(len(missingTypeTitle)):
                validity_file.write(f"**{str(missingTypeTitle[i])}**" + " ( ID: " + str(missingType[i]) + "), " )
            validity_file.write("Please delete or add type to these ERs using `Update a ER` option")
            validity_file.write("\n")

        if(len(missingDes) != 0):
            self.num = self.num + 1
            validity_file.write(str(self.num)+". The following ERs are missing both description and url: " )
            for i in range(len(missingDes)):
                validity_file.write(f"**{str(missingDesTitle[i])}**" + " ( ID: " + str(missingDes[i]) + "), ")
            validity_file.write("Please delete these ERs or update one of these fields using `Update a ER` option")
            validity_file.write("\n")

        if(len(missingAssesses) != 0):     
            self.num = self.num + 1
            validity_file.write(str(self.num)+". The following ERs are missing an Assesses Relationship : " )
            for i in range(len(missingAssesses)):
                validity_file.write(f"**{str(missingAssessesTitle[i])}**" + " ( Type: " + str(missingAssessType[i]) + ", ID: " + str(missingAssesses[i]) + "), ")
            validity_file.write("Please create an `Assesses` relation using `Modify Relation'")
            validity_file.write("\n")
        
        if(len(missingComesAfter) != 0):
            self.num = self.num + 1
            validity_file.write(str(self.num)+". The following ERs are missing a Comes After Relationship : " )
            for i in range(len(missingComesAfter)):
                validity_file.write(f"**{str(missingCATitle[i])}**"  + " ( Type: " + str(missingCAType[i]) + ", ID: " + str(missingComesAfter[i]) + "), " )
            validity_file.write("Please create an `comes After` relation using `Modify Relation")
            validity_file.write("\n")
        
        if(len(missingIsPartOf) != 0 ):
            self.num = self.num + 1
            validity_file.write(str(self.num)+". The following ERs are missing a IsPartOf Relationship : " )
            for i in range(len(missingIsPartOf)):
                validity_file.write(f"**{str(missingIPTitle[i])}**" + " ( Type: " + str(missingIPType[i]) + ", ID: " + str(missingIsPartOf[i]) + "), ")
            validity_file.write("These ERs must be part of a composite ER! Please create an `is Part of` relation using `Modify Relation")
            validity_file.write("\n")

        validity_checker.__check_comesAfter_validity(self, validity_file)
        validity_checker.__check_assesses_validity(self, validity_file)
        validity_checker.__check_isPartOf_validity(self, validity_file)
        validity_file.close()

    def __check_isPartOf_validity(self, report_file):
        # only atomic ERs must have isPartOf
        # atomics can have requires or isPartOf (or both) but cannot have assesses or comesAfter --> taken care of by datasetCreator
        pass

    def __check_assesses_validity(self, report_file):
        # make sure the assesses relation is only between rER and aER
        # all rER must assess one aER

        # first check that only rERs have assesses relations:
        for i in range(len(self.df.index)):
            node_type = self.df["type"][i]; title = self.df["title"][i]; n_id = self.df["identifier"][i]
            try: assess = int(self.df["assesses"][i])
            except: assess = None
            if assess != None:
                if node_type != "rER":
                    self.num = self.num + 1
                    report_file.write(str(self.num)+". Er `" + str(title)+ "` | ID: "+ str(n_id)+ "| type: " + str(node_type) + " cannot assess another ER"+ "| Please use `update a node` or `modify relation` option to fix this relation!")

        # 2nd check that all rERs are assessing an aER
        for i in range(len(self.df.index)):
            node_type = self.df["type"][i]; title = self.df["title"][i]; n_id = self.df["identifier"][i]
            if node_type == "rER":
                try: assess = int(self.df["assesses"][i])
                except: assess = None
                if assess != None:
                    for j in range(len(self.df.index)):
                        aER_id = self.df["identifier"][j]; 
                        if assess == aER_id:
                            aER_type = self.df["type"][j]; aER_title = self.df["title"][j]
                            if(aER_type != "aER"):
                                self.num = self.num + 1
                                report_file.write(str(self.num)+". Er `" + str(title)+ "` | ID: "+ str(n_id)+ "| type: " + str(node_type) + " cannot assess: "+ str(aER_title)+ ", ID: "+str(aER_id)+" of type "+str(aER_type)+ "| Please use `update a node` or `modify relation` option to fix this relation!")
                            break

        # 3rd check that assesses value of rERs are a set and report for duplicates
        # already checked by visualizer --> datasetcreator set multiple relations for ca, assesses, isPart of to empty
        

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
                        report_file.write(str(self.num)+". Multiple ERs come after `" + str(title)+ "` | ID: "+ str(n_id)+ "| type: " + str(node_type) + ": "+problematic_nodes +"| Please fix some of these relation by removing node in `update a node` or updating comesAFter relation in `modify relation` option!")
                        break
        # check for broken comesAfter
        ca_is_broken = True
        # check that start is referred at least once
        for i in range(len(self.df.index)):
            node_type = self.df["type"][i]
            if node_type == "aER" or node_type == "iER" or node_type == "end":
                try: ca = int(self.df["comesAfter"][i])
                except: ca = None
                if ca == 0:
                    ca_is_broken = False
                    break
        for i in range(len(self.df.index)):
            node_type = self.df["type"][i]
            if node_type == "aER" or node_type == "iER" or node_type == "end":
                try: ca = int(self.df["comesAfter"][i])
                except: ca = None
                if ca == None:
                    ca_is_broken = True
        
        #check if end node is being referred in the CA field
        for i in range(len(self.df.index)):
            try: ca = int(self.df["comesAfter"][i])
            except: ca = None
            end_node = self.df["identifier"][len(self.df.index)-1]
            if ca == end_node:
                self.num = self.num + 1
                report_file.write(str(self.num)+". There is node after the END node! \n")
                
        if ca_is_broken:
            self.num = self.num + 1
# <<<<<<< nias_branch
            report_file.write(str(self.num)+". The Learning Path is broken! please fix comesAfter relations so we have a learning path!")
                       
# =======
#             report_file.write(str(self.num)+". The Learning Path is broken! please fix comesAfter relations so we have a learning path! \n")

            

# >>>>>>> development
    def clear_report(self):
        open(self.validity_file_name, 'w').close()
        self.num = 0