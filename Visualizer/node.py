

class Node:
    ##input er is a dict object. the spelling of the columns are important but the their order is not important. 
    # each row of the dataset represents a single node. currently accessed directly-- set getters and setters when possible. 

    def __init__(self,er):
        # the following have to exist and be non empty
        #A unique integer that identifies the ER
        try: # remove except clause when the all datasets have identifier field instead of id
            self.er_id = er["identifier"]
        except:
            self.er_id = er["id"]
        # title to be displayed
        self.er_title = er["title"]
        #he type of composite ER (e.g. iER), atomic ER (.pdf), start/ end
        self.er_type = er["type"]    

        #at least one of the following must be non-empty
        # A text description for the resource 
        try:
            self.er_description = er["description"]
        except:
            self.er_description = ""
        #The URL associated with this ER
        try:
            self.er_url = er["url"]
        except:
            self.er_url = ""     

        # the following may or may not be in data set and they represent the relations (aka arrows)
        # try:
        #     self.er_alternative = er["alternative"]
        # except:
        #     self.er_alternative = ""
        #A requires B. verse of isRequiredBy
        try:
            self.er_requires = er["requires"]
        except:
            self.er_requires = ""
        #B isRequiredBy A: The inverse relation of requires
        try:
            self.er_is_required_by = er["isrequiredby"]
        except:
            self.er_is_required_by = ""
        #A references B. 
        try:
            self.er_references = er["references"]
        except:
            self.er_references = ""
        #A isReferencedBy B
        try:
            self.er_is_referenced_by = er["isreferencedby"]
        except:
            self.er_is_referenced_by = ""
        #A isFormatOf B
        try:
            self.er_is_format_of = er["isformatof"]
        except:
            self.er_is_format_of = ""
        #B isPartOf A
        try:
            self.er_isPartOf = er["ispartof"]
        except:
            self.er_isPartOf = ""
        #A hasPart B
        try:
            self.er_has_part = er["haspart"]
        except:
            self.er_has_part = ""
        #A comesAfter B
        try:
            self.er_comesAfter = er["comesafter"]
        except:
            self.er_comesAfter = ""
        #B comesBefore A
        try:
            self.er_comesBefore = er["comesbefore"]
        except:
            self.er_comesBefore = "" 
        #R assesses A
        try:
            self.er_assesses = er["assesses"]
        except:
            self.er_assesses = ""
        #A isAssessedBy R
        try:
            self.er_is_assessed_by = er["isassessedby"]
        except:
            self.er_is_assessed_by = ""

        #time
        try:
            self.er_duration = int(er["duration"])
        except:
            self.er_duration = 0

        #x position
        try:
            self.er_x_value = int(er["x values"])
        except:
            self.er_x_value = ""
        
        #y position
        try:
            self.er_y_value = int(er["y values"])
        except:
            self.er_y_value = ""

        
    
        