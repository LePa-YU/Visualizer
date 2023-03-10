

class Node:
    ##input er is a dict object. the spelling of the columns are important but the their order is not important
    def __init__(self,er):
        # the following have to exist and be non empty
        self.er_id = er["id"]
        self.er_title = er["title"]
        self.er_type = er["type"]
        # the following may or may not be in data set
        try:
            self.er_alternative = er["alternative"]
        except:
            self.er_alternative = ""
        try:
            self.er_url = er["targeturl"]
        except:
            self.er_url = ""
        try:
            self.er_isPartOf = er["ispartof"]
        except:
            self.er_isPartOf = ""
        try:
            self.er_assesses = er["assesses"]
        except:
            self.er_assesses = ""
        try:
            self.er_comesAfter = er["comesafter"]
        except:
            self.er_comesAfter = ""
        try:
            self.er_requires = er["requires"]
        except:
            self.er_requires = ""
