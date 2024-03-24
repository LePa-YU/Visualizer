
# This class instantiate the colors used for different components of the network:
# aER: Activity ER | default: #FF7273
# rER: rubric ER | default: #FF7273
# iER: instructional ER | default: #F69159
# general: any nodes that are not one of specified/ atomic ER with type zip | default: #ECD19A
# assesses: assess/ is assessed by relationship | default: #FF7273
# comesAfter: comes after / comes before relation ship | default: #C0CB6B
# isPartOf: is part of/ has part relationship | default: #ECD19A
# start: start node | default: #C0CB6B
# end: end node | default: #C0CB6B
# requires: requires/ is required by relation | default: #BF87F2
# aImg: atomic ERs with .png/.jpeg types | default: #A24052
# aMov: atomic ERs with .mov/.mp4 | default: #FBF495
# aSW: atomic ERs with exe/ipynd/app types | default: #93C539
# aAudio: atomic ERs with mp3/wav types |  default: #437C6C
# aText: atomic ERs with txt/pdf/html/md/pptx/dvi |  default: #20C18B
# aDataset: atomic ERs with csv/ xlsx |  default:  #5FC7D3

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
        