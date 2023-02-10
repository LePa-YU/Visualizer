

def setData(data_list ):
    global data
    data = data_list

def getToolTip(d_id, d_title, d_isPartOf, d_url):
    text = ""
      # finding the type of the container
    er_container = data[d_isPartOf] ## contains id and type
    er_type = er_container[1]
    if(er_type == "iER"):
        text = text + "Instructional ER \n\n"
        # type of the atomic ER e.g. ebook, video,...
        type = " NA \n"
        text += "Type:"+type
        # name of the atomic ER
        text += "Name: " + d_title + "\n"
    elif(er_type == "aER"):
        text = text + "Activity ER \n\n"
        text += "Name: " + d_title + "\n"
        assumes = "NA\n"
        text+="Assumes: " + assumes
    elif(er_type == "rER"):
        text = text + "Rubric ER\n\n"
        er_assesses = er_container[2]
        text += "Assessment of aER" + str(int(er_assesses))+"\n"
        grade = "NA \n"
        text += "Grades: " + grade

    text += "Available link: "
    if(d_url != "nil"):
        text += d_url +"\n"
    else:
        text += "NA \n"  
    # adding unique id 
    unique_id = er_type + str(d_id)
    text += "ID: "+ unique_id
    
    return text