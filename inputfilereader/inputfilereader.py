print("\033[H\033[J")

import mbsObject

f = open("inputfilereader/test.fdd","r")

fileContent = f.read().splitlines()
f.close()

numOfRigidBodies = 0
numOfConstraints = 0
currentBlockType = ""
currentTextBlock = []
listOfMbsObjects = []
search4Objects = ["RIGID_BODY", "CONSTRAINT"]



#Search Number of Rigid Bodies 
for line in fileContent:
    if(line.find("$") >= 0):    #new Block found
        if(currentBlockType != ""):
            if(currentBlockType == "RIGID_BODY"):
                listOfMbsObjects.append(mbsObject.mbsObject("body", currentTextBlock))
            currentBlockType = ""


    for type_i in search4Objects:   #Sucht nach Schlagwörtern
        if(line.find(type_i, 1, len(type_i) +1) >= 0):
            currentBlockType = type_i
            currentTextBlock.clear()
            break
    currentTextBlock.append(line)

print(len(listOfMbsObjects))