print("\033[H\033[J")

import mbsObject
import json

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
                listOfMbsObjects.append(mbsObject.rigidBody(currentTextBlock))
            currentBlockType = ""


    for type_i in search4Objects:   #Sucht nach Schlagwörtern
        if(line.find(type_i, 1, len(type_i) +1) >= 0):
            currentBlockType = type_i
            currentTextBlock.clear()
            break
    currentTextBlock.append(line)

modelObjects = []
for object in listOfMbsObjects:
    modelObjects.append(object.parameter)


jDataBase = json.dumps({"modelObjects": modelObjects})
with open ("inputfilereader/test.vis3", "w") as outfile:
    outfile.write(jDataBase)

jDataBase = json.dumps({"modelObjects": modelObjects})  #mit alt + shift + f zum trukturieren
with open ("inputfilereader/test.json", "w") as outfile:
    outfile.write(jDataBase)

f = open("inputfilereader/test.json", "r")
data = json.load(f)
f.close()


fds = open("inputfilereader/test.fds","w")  #w für write (Wird erstellt) | a für append (Bereits vorhandenes File)
for mbsObject_i in listOfMbsObjects:
    mbsObject_i.writeInputfile(fds)
fds.close()

print(len(listOfMbsObjects))