
class mbsObject:
    def __init__(self,type,subtype,text,parameter):
        self.__type = type
        self.__subtype = subtype
        self.parameter = parameter

        for line in text:
            splitted = line.split(":")
            for key in parameter.keys():
                if(splitted[0].strip() == key):
                    if(parameter[key]["type"] == "float"):
                        parameter[key]["value"] = self.str2float(splitted[1])
                    elif(parameter[key]["type"] == "vector"):
                        parameter[key]["value"] = self.str2vector(splitted[1])
                    elif(parameter[key]["type"] == "vectorInt"):
                        parameter[key]["value"] = self.str2vectorInt(splitted[1])
                    elif(parameter[key]["type"] == "int"):
                        parameter[key]["value"] = self.str2int(splitted[1])
                    elif(parameter[key]["type"] == "string"):
                        parameter[key]["value"] = splitted[1].strip()
                    elif(parameter[key]["type"] == "bool"):
                        parameter[key]["value"] = self.str2bool(splitted[1])

    
    def writeInputfile(self,file):
        text = []
        text.append(self.__type + " " + self.__subtype + "\n")
        for key in self.parameter.keys():
            #Umwandlung Float in String
            if(self.parameter[key]["type"] == "float"):
                text.append("\t"+key+" = "+self.float2str(self.parameter[key]["value"])+"\n")

            if(self.parameter[key]["type"] == "vector"):
                text.append("\t"+key+" = "+self.vector2str(self.parameter[key]["value"])+"\n")

            if(self.parameter[key]["type"] == "vectorInt"):
                text.append("\t"+key+" = "+self.vectorInt2str(self.parameter[key]["value"])+"\n")

            if(self.parameter[key]["type"] == "int"):
                text.append("\t"+key+" = "+self.int2str(self.parameter[key]["value"])+"\n")

            if(self.parameter[key]["type"] == "string"):
                text.append("\t"+key+" = "+self.parameter[key]["value"]+"\n")

            if(self.parameter[key]["type"] == "bool"):
                text.append("\t"+key+" = "+self.bool2str(self.parameter[key]["value"])+"\n")

                

            



        text.append("End"+self.__type+"\n%\n")

        file.writelines(text)


    def str2float(self,inString):
        return float(inString)
    def float2str(self,inFloat):
        return str(inFloat)
    
    def str2int(self,inString):
        return int(inString)
    def int2str(self,inInt):
        return str(inInt)
    
    def str2bool(self, inString):
        return bool(inString)
    def bool2str(self, inBool):
        return str(inBool)
    
    def str2vector(self,inString):
        return [float(inString.split(",")[0]),float(inString.split(",")[1]),float(inString.split(",")[2])]
    
    def str2vectorInt(self,inString):
        return [int(inString.split()[0]),int(inString.split()[1]),int(inString.split()[2])]

    def vector2str(self,inVector):
        return str(inVector[0]) + "," + str(inVector[1]) + "," + str(inVector[2])
    
    def vectorInt2str(self,inVector):
        return str(inVector[0]) + " " + str(inVector[1]) + " " + str(inVector[2])
    
class rigidBody(mbsObject):
    def __init__(self,text):
        parameter = {
            "name": {"type": "string", "value": "empty"},
            "mass": {"type": "float", "value": 1.},
            "COG": {"type": "vector", "value": [0.,0.,0.]},

            "position": {"type": "vector", "value": [0.,0.,0.]},
            "color": {"type": "vectorInt", "value": [0,0,0] },
            "transparency": {"type": "int", "value": 1}
        }

        mbsObject.__init__(self,"Body","Rigid_EulerParameter_PAI",text,parameter)

class constraint(mbsObject):
    def __init__(self,text):
        parameter = {
            "name": {"type": "string", "value": "empty"},
            "body1": {"type": "string", "value": "empty"},
            "body2": {"type": "string", "value": "empty"},
            "position": {"type": "vector", "value": [0.,0.,0.]},

            "dx": {"type": "bool", "value": 0},
            "dy": {"type": "bool", "value": 0},
            "dz": {"type": "bool", "value": 0},
            "ax": {"type": "bool", "value": 0},
            "ay": {"type": "bool", "value": 0},
            "az": {"type": "bool", "value": 0}

        }

        mbsObject.__init__(self,"Constraint","Rigid_EulerParameter_PAI",text,parameter)