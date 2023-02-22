

class Node:
    ##input er is a dict object. the spelling of the columns are important but the their order is not important
    def __init__(self,er):
       print(er)
       self.er_id = er["ID"]
       self.er_title = er["Title"]
       self.er_alternative = er["Alternative"]
       self.er_url = er["targetUrl"]
       self.er_type = er["Type"]
       self.er_isPartOf = er["isPartOf"]
       self.er_assesses = er["assesses"]
       self.er_comesAfter = er["comesAfter"]
