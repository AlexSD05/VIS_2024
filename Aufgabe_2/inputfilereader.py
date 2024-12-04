import mbsObject
import json

def readInputFile(filePath):

    #f = open("inputfilereader/test.fdd","r")
    f = open(filePath,"r")
    fileContent = f.read().splitlines()
    f.close()

    currentBlockType = ""
    currentTextBlock = []
    listOfMbsObjects = []
    search4Objects  = ["RIGID_BODY", "CONSTRAINT", "FORCE_GenericForce", "FORCE_GenericTorque", "DATAOBJECT_PARAMETER", "MEASURE"]

    for line in fileContent:
        if(line.find("$") >= 0):#new block found
            if(currentBlockType != ""):
                if(currentBlockType == "RIGID_BODY"):
                    listOfMbsObjects.append(mbsObject.rigidBody(currentTextBlock))
                
                elif(currentBlockType == "CONSTRAINT"):
                    listOfMbsObjects.append(mbsObject.constraint(currentTextBlock))

                elif(currentBlockType == "FORCE_GenericForce"):
                    listOfMbsObjects.append(mbsObject.genericforce(currentTextBlock))

                elif(currentBlockType == "FORCE_GenericTorque"):
                    listOfMbsObjects.append(mbsObject.generictorque(currentTextBlock))

                elif(currentBlockType == "DATAOBJECT_PARAMETER"):
                    listOfMbsObjects.append(mbsObject.dataobjectparameter(currentTextBlock))

                elif(currentBlockType == "MEASURE"):
                    listOfMbsObjects.append(mbsObject.measure(currentTextBlock))

                currentBlockType = ""

        for type_i in search4Objects:
            if(line.find(type_i,1,len(type_i)+1) >= 0):
                currentBlockType = type_i
                currentTextBlock.clear()
                break
        
        currentTextBlock.append(line)

    print("Number of objects = ", len(listOfMbsObjects))


    #import/export functionality (for later use in model.py)
    modelObjects = []
    for object in listOfMbsObjects:
        modelObjects.append(object.parameter)
    jDataBase = json.dumps({"modelObjects": modelObjects})
    with open("Aufgabe_2/test.json", "w") as outfile:
        outfile.write(jDataBase)

    f = open("Aufgabe_2/test.json","r")
    data = json.load(f)
    f.close()

    fds = open("Aufgabe_2/test.fds","w")
    for mbsObject_i in listOfMbsObjects:
        mbsObject_i.writeInputfile(fds)
    fds.close()

    return listOfMbsObjects
    #-------------------------------------------------------