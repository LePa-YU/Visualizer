

class Node:
    ##input er is a dict object. the spelling of the columns are important but the their order is not important
    def __init__(self,er):
       print(er)
       self.er_id = er["id"]
       self.er_title = er["title"]
       self.er_alternative = er["alternative"]
       self.er_url = er["targeturl"]
       self.er_type = er["type"]
       self.er_isPartOf = er["ispartof"]
       self.er_assesses = er["assesses"]
       self.er_comesAfter = er["comesafter"]
