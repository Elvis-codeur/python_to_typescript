import os 
import json 
import ast 
from my_tools.general import read_file



class BaseType():
    def __init__(self,name,type_) -> None:
        self.name = name
        self.type_ = type_ 
    def __repr__(self) -> str:
        return "{}({})".format(self.__class__.__name__,self.__dict__)

class StringType(BaseType):
    def __init__(self, name) -> None:
        super().__init__(name)

class NumberType(BaseType):
    def __init__(self, name) -> None:
        super().__init__(name)

class DateType(BaseType):
    def __init__(self, name) -> None:
        super().__init__(name)
    
class BooleanType(BaseType):
    def __init__(self, name) -> None:
        super().__init__(name) 

class AnyType(BaseType):
    def __init__(self, name) -> None:
        super().__init__(name) 

class ChoiceFieldType(BaseType):
    def __init__(self, name) -> None:
        super().__init__(name)

class ForeignKeyType(BaseType):
    def __init__(self, name) -> None:
        super().__init__(name)

class OneToOneFieldType(BaseType):
    def __init__(self, name) -> None:
        super().__init__(name)

class JSONFieldType(BaseType):
    def __init__(self, name) -> None:
        super().__init__(name)

class BinaryFieldType(BaseType):
    def __init__(self, name) -> None:
        super().__init__(name)

class ManyToManyFieldType(BaseType):
    def __init__(self, name) -> None:
        super().__init__(name)

class FileFieldType(BaseType):
    def __init__(self, name) -> None:
        super().__init__(name)
    
class FilePathFieldType(BaseType):
    def __init__(self, name) -> None:
        super().__init__(name)

class ImageFieldType(BaseType):
    def __init__(self, name) -> None:
        super().__init__(name)


TYPE_MAP = {
    "UUIDField": StringType,
    "OneToOneField": OneToOneFieldType,
    "PositiveIntegerField": NumberType,
    "DecimalField": NumberType,
    "BooleanField": BooleanType,
    "CharField": StringType,
    "TextField": StringType,
    "DateField": DateType,
    "ChoiceField": ChoiceFieldType,
    "ForeignKey": ForeignKeyType,
    "ManyToManyField": ManyToManyFieldType,
    "JSONField": JSONFieldType,
    "AutoField": NumberType,
    "BigIntegerField": NumberType,
    "BinaryField": BinaryFieldType,
    "DateTimeField": DateType,
    "DurationField": DateType,
    "EmailField": StringType,
    "FileField": FileFieldType,
    "FilePathField": FilePathFieldType,
    "FloatField": NumberType,
    "GenericIPAddressField": StringType,
    "ImageField": ImageFieldType,
    "IntegerField": NumberType,
    "IPAddressField": StringType,
    "NullBooleanField": BooleanType,
    "PositiveSmallIntegerField": NumberType,
    "str":StringType,
    "float":NumberType,
    "int":NumberType,
}

class RepresentationObject():
    def __init__(self,name) -> None:
        self.name = name

    def __repr__(self) -> str:
        return "{}({})".format(self.__class__.__name__,self.__dict__)
    

class ClassRepresentation(RepresentationObject):
    def __init__(self, name) -> None:
        super().__init__(name)
        self.attributes = []
        self.functions = []
        self.subclasses = []

    
    
class FunctionRepresentation(RepresentationObject):
    def __init__(self, name) -> None:
        super().__init__(name)


class FileRepresentation(RepresentationObject):
    def __init__(self, name,path) -> None:
        super().__init__(name)
        self.classes = []
        self.functions = []
        self.imports = []
        self.path = path



def analyse_function_def(node:ast.FunctionDef):
    func_object = FunctionRepresentation(node.__dict__["name"])           
    if node.__dict__["returns"]:
        returns = node.__dict__["returns"]
        
        if type(returns) == ast.List:
            a = 0
        elif type(returns) == ast.Set:
            a = 0
        else:
            if type(returns) == ast.Attribute:
                func_object.__dict__["returns"] = {
                    "type":"attribute",
                    "attr": returns.__dict__["attr"]
                }
            elif type(returns) == ast.Name:
                func_object.__dict__["returns"] = {
                    "type":"name",
                    "id": returns.__dict__["id"]
                }
    else:
        func_object.__dict__["returns"] = {
                    "type":"unknown",
                }
        
    return func_object

def analyse_class_def(node:ast.ClassDef):
    cls = ClassRepresentation(name=node.__dict__.get("name"))
    for class_def in node.body:
        if type(class_def) == ast.Assign: # Les attributs de la classe
            nom_variable = class_def.__dict__["targets"][0].__dict__["id"]
            #print(class_def.__dict__["value"].__dict__,nom_variable)

            if type(class_def.__dict__["value"]) is ast.Name:
                type_variable = class_def.__dict__["value"].__dict__['id']
            elif type(class_def.__dict__["value"]) is ast.Call:

                if type(class_def.__dict__["value"].__dict__['func']) == ast.Attribute:
                    type_variable = class_def.__dict__["value"].__dict__['func'].__dict__["attr"]
                elif type(class_def.__dict__["value"].__dict__['func']) == ast.Name:
                    type_variable = class_def.__dict__["value"].__dict__['func'].__dict__['id']
            
            elif type(class_def.__dict__["value"]) is ast.List:
                type_variable = "list"

            elif type(class_def.__dict__["value"]) is ast.Set:
                type_variable = "set"

            elif type(class_def.__dict__["value"]) is ast.Tuple:
                type_variable = "tuple"
            
            #print(nom_variable,type_variable)
            type_script_object = BaseType(nom_variable,type_variable)

            type_script_object.__dict__["keywords"] = {}
            type_script_object.__dict__["args"] = []

        
            if type_variable: # Les méthodes de la classe 
                if type(class_def.__dict__["value"]) is ast.Call: # Un call est une instantiation de la variable à base de fonction ou de classes 
                    for keyword in class_def.__dict__["value"].__dict__["keywords"]:
                        #print(keyword.__dict__)
                        if keyword != None:
                            if type(keyword.__dict__["value"]) == ast.Constant:
                                type_script_object.__dict__["keywords"][keyword.__dict__["arg"]] = keyword.__dict__["value"].__dict__['value']
                            elif type(keyword.__dict__["value"]) == ast.Name:
                                type_script_object.__dict__["keywords"]["id"] =  keyword.__dict__["value"].__dict__['id']

                    for arg in class_def.__dict__["value"].__dict__["args"]:
                        type_script_object.__dict__["args"].append(arg.__dict__["value"])
                        
                elif type(class_def.__dict__["value"]) is ast.List:
                    elts = []
                    for ob in class_def.__dict__["value"].__dict__["elts"]:
                        if type(ob) == ast.Constant:
                            elts.append(ob.__dict__['value'])
                        else:
                            raise ValueError(f"The list {nom_variable} containt on constant element ")
                    type_script_object.__dict__["elts"] = elts
                            
                    
        

                    
                
            cls.attributes.append(type_script_object) 
        
        elif type(class_def) == ast.FunctionDef:
            func_object = analyse_function_def(class_def)
            cls.functions.append(func_object) 

        elif type(class_def) == ast.ClassDef:
            cls.subclasses.append(analyse_class_def(class_def))
            
    return cls 

                    
    

def analyse_file(file_path):
    code = read_file(file_path)
    parsed = ast.parse(code)

    file_name = os.path.splitext(os.path.basename(file_path))[0] # Le nom du fichier sans exention

    result = FileRepresentation(file_name,os.path.dirname(file_path))

    for node in parsed.body:
        #print(node)
        if type(node) is ast.ClassDef: # Les classes du fichier
            a = 0
            result.classes.append(analyse_class_def(node))
        elif type(node) == ast.FunctionDef:
            result.functions.append(analyse_function_def(node))
    return result


def test1():
    filename = "tests/test_python_to_typescript/test1/models.py"
    print(analyse_file(filename))

            

if __name__ == "__main__":
    test1()