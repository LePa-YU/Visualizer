
class Color:
    def __init__(self, aER, rER, iER, general, assesses, comesAfter, isPartOf, start, end, requires, aImg, aMov, aSW, aAudio, aText, aDataset):
        self.aER_node_color = aER
        self.rER_node_color = rER
        self.iER_node_color = iER
        
        self.assess_relationship_color = assesses
        self.comesAfter_relationship_color = comesAfter
        self.isPartOf_relationship_color = isPartOf
        self.start_node_color = start
        self.end_node_color = end
        self.requires_node_color = requires
        
        self.atomic_node_color_img =  aImg #.png, .jpeg 
        self.atomic_node_color_mov =  aMov #.mov, .mp4
        self.atomic_node_color_software =  aSW #.exe, .ipynd, .app
        self.atomic_node_color_audio =  aAudio #.mp3, .wav
        self.atomic_node_color_text =  aText #.txt, .pdf, .html, .md, .pptx, .dvi
        self.atomic_node_color_dataset =  aDataset #.csv, .xlsx
        self.atomic_node_color_coll = general #.zip
        