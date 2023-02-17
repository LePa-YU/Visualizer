

class Node:
    ##input er is a tuple containing data from single row of input CSV file
    # er[0]: ID
    # er[1]: title
    # er[2]: alternative
    # er[3]: targetUrl
    # er[4]: Type
    # er[5]: isPartOf
    # er[6]: assesses
    # er[7]: comesAfter
    def __init__(self,er):
       self.er_id = er[0]
       self.er_title = er[1]
       self.er_alternative = er[2]
       self.er_url = er[3]
       self.er_type = er[4]
       self.er_isPartOf = er[5]
       self.er_assesses = er[6]
       self.er_comesAfter = er[7]
