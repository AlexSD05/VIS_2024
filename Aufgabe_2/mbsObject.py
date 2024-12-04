
"""Aktuellster Stand des mbsObject Files"""

import vtk


class mbsObject:
    def __init__(self,type,subtype,text,parameter):
        self.__type = type
        self.__subtype = subtype
        self.parameter = parameter

        self.actor = vtk.vtkActor()

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

                    #Einlesen der Freiheitsgrade
                    elif(parameter[key]["type"] == "bool"):
                        parameter[key]["value"] = self.str2bool(splitted[1])

                    #Einlesen des Dateipfades
                    elif(parameter[key]["type"] == "path"):
                        parameter[key]["value"] = self.str2path(splitted[1].strip(), splitted[2])
                        
                        #Test Ausgabe eines Parameters
                        #print(self.parameter["geometry"]["value"])


    #Funktion zur Ausgabe der Objekte
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

            #Freiheitsgrade
            if(self.parameter[key]["type"] == "bool"):
                text.append("\t"+key+" = "+self.bool2str(self.parameter[key]["value"])+"\n")
            
            #Dateipfad
            if(self.parameter[key]["type"] == "path"):
                text.append("\t"+key+" = "+self.parameter[key]["value"]+"\n")
                

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
    
    
    
    def str2path(self, inStorage, inPath):
        return str(inStorage) + ":" + str(inPath)
    
    

# Class für RIGID_BODY
class rigidBody(mbsObject):
    def __init__(self,text):
        parameter = {
            "name": {"type": "string", "value": "empty"},
            "geometry": {"type": "path", "value": "empty"},
            "position": {"type": "vector", "value": [0.,0.,0.]},
            "x_axis": {"type": "vector", "value": [0.,0.,0.]},
            "y_axis": {"type": "vector", "value": [0.,0.,0.]},
            "z_axis": {"type": "vector", "value": [0.,0.,0.]},
            "color": {"type": "vectorInt", "value": [0,0,0] },
            "transparency": {"type": "int", "value": 1},
            "mass": {"type": "float", "value": 1.},
            "COG": {"type": "vector", "value": [0.,0.,0.]}           
        }

        mbsObject.__init__(self,"Body","Rigid_EulerParameter_PAI",text,parameter)

#------------------------------------------------------------------------------
# Code für VTK       
        
        # Einlesen der Geometrie
        reader = vtk.vtkOBJReader()
        reader.SetFileName(self.parameter["geometry"]["value"])
        reader.Update()

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(reader.GetOutputPort())

        # Actor erstellen
        self.actor.SetMapper(mapper)
        self.actor.GetProperty().SetColor(self.parameter["color"]["value"])
        self.actor.GetProperty().SetOpacity(self.parameter["transparency"]["value"]/100) # Transparentz übernehmen/ einstellen 

        # Transformation basierend auf der Position und Orientierung
        self.apply_transformations()


    def apply_transformations(self):
        """Wendet die Position und Orientierung an den Actor an."""
        transform = vtk.vtkTransform()
        
        # Setze Translation
        pos = self.parameter["position"]["value"]
        transform.Translate(pos[0], pos[1], pos[2])

        # Setze Orientierung (Rotationsmatrix aus x_axis, y_axis, z_axis)
        x_axis = self.parameter["x_axis"]["value"]
        y_axis = self.parameter["y_axis"]["value"]
        z_axis = self.parameter["z_axis"]["value"]
        transform.Concatenate([x_axis[0], y_axis[0], z_axis[0], 0,
                               x_axis[1], y_axis[1], z_axis[1], 0,
                               x_axis[2], y_axis[2], z_axis[2], 0,
                               0, 0, 0, 1])

        # Transformation dem Actor zuweisen
        self.actor.SetUserTransform(transform)
#------------------------------------------------------------------------------

# Klasse für Constraints
class constraint(mbsObject):
    def __init__(self,text):
        parameter = {
            "name": {"type": "string", "value": "empty"},
            "body1": {"type": "string", "value": "empty"},
            "body2": {"type": "string", "value": "empty"},
            "dx": {"type": "bool", "value": 0},
            "dy": {"type": "bool", "value": 0},
            "dz": {"type": "bool", "value": 0},
            "ax": {"type": "bool", "value": 0},
            "ay": {"type": "bool", "value": 0},
            "az": {"type": "bool", "value": 0},
            "position": {"type": "vector", "value": [0.,0.,0.]},
            "x_axis": {"type": "vector", "value": [0.,0.,0.]},
            "y_axis": {"type": "vector", "value": [0.,0.,0.]},
            "z_axis": {"type": "vector", "value": [0.,0.,0.]}

            

        }

        mbsObject.__init__(self,"Constraint","Rigid_EulerParameter_PAI",text,parameter)


class genericforce(mbsObject):
    def __init__(self,text):
        parameter = {
            "name": {"type": "string", "value": "empty"},
            "body1": {"type": "string", "value": "empty"},
            "body2": {"type": "string", "value": "empty"},
            "PointOfApplication_Body1": {"type": "vector", "value": [0.,0.,0.]},
            "PointOfApplication_Body2": {"type": "vector", "value": [0.,0.,0.]}, 
            "mode": {"type": "string", "value": "empty"},  
            "direction": {"type": "vector", "value": [0.,0.,0.]},   
            "ForceExpression": {"type": "string", "value": "empty"}    
        }

        mbsObject.__init__(self,"GenericForce","Rigid_EulerParameter_PAI",text,parameter)

class generictorque(mbsObject):
    def __init__(self,text):
        parameter = {
            "name": {"type": "string", "value": "empty"},
            "body1": {"type": "string", "value": "empty"},
            "body2": {"type": "string", "value": "empty"},
            "mode": {"type": "string", "value": "empty"},  
            "direction": {"type": "vector", "value": [0.,0.,0.]},   
            "TorqueExpression": {"type": "string", "value": "empty"}    
        }

        mbsObject.__init__(self,"GenericTorque","Rigid_EulerParameter_PAI",text,parameter)

class dataobjectparameter(mbsObject):
    def __init__(self,text):
        parameter = {
            "name": {"type": "string", "value": "empty"},
            "InitialValue": {"type": "float", "value": 0.}    
        }

        mbsObject.__init__(self,"DATAOBJECT_PARAMETER","Rigid_EulerParameter_PAI",text,parameter)

class measure(mbsObject):
    def __init__(self,text):
        parameter = {
            "name": {"type": "string", "value": "empty"},
            "body1": {"type": "string", "value": "empty"},
            "body2": {"type": "string", "value": "empty"},
            "type": {"type": "string", "value": "empty"},  
            "component": {"type": "int", "value": 0},   
            "location_body1": {"type": "vector", "value": [0.,0.,0.]},
            "location_body2": {"type": "vector", "value": [0.,0.,0.]},
            "use_initial_value": {"type": "float", "value": 0.}
        }

        mbsObject.__init__(self,"MEASURE","Rigid_EulerParameter_PAI",text,parameter)
