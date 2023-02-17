
class Color:
    def __init__(self, aER, rER, iER, general, assesses, comesAfter, isPartOf, start, end):
        self.aER_node_color = aER
        self.rER_node_color = rER
        self.iER_node_color = iER
        self.atomic_node_color = general
        self.assess_relationship_color = assesses
        self.comesAfter_relationship_color = comesAfter
        self.isPartOf_relationship_color = isPartOf
        self.start_node_color = start
        self.end_node_color = end
        