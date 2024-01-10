import os 
import json 
import ast 
from my_tools.general import read_file



class BaseType():
    def __init__(self,name) -> None:
        self.name = name
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
}



class ClassRepresentation():
    def __init__(self,name) -> None:
        self.name = name
        self.attributes = []

    def __repr__(self) -> str:
        return "ClassRepresentation({})".format(self.__dict__)
    

def test1():
    filename = "tests/test_python_to_typescript/test1/models.py"
    code = read_file(filename)
    parsed = ast.parse(code)
    for node in parsed.body:
        if type(node) is ast.ClassDef:
            cls = ClassRepresentation(name=node.__dict__.get("name"))
            for class_def in node.body:
                if type(class_def) == ast.Assign:
                    nom_variable = class_def.__dict__["targets"][0].__dict__["id"]
                    type_variable = class_def.__dict__["value"].__dict__['func'].__dict__["attr"]
                    #print(nom_variable,type_variable)
                    type_script_object = TYPE_MAP[type_variable](nom_variable)

                    type_script_object.__dict__["keywords"] = {}
                    type_script_object.__dict__["args"] = []

                    if type_variable:
                       #print(class_def.__dict__["value"].__dict__)
                        for keyword in class_def.__dict__["value"].__dict__["keywords"]:
                            #print(keyword.__dict__)
                            if keyword != None:
                                if type(keyword.__dict__["value"]) == ast.Constant:
                                   type_script_object.__dict__["keywords"][keyword.__dict__["arg"]] = keyword.__dict__["value"].__dict__['value']
                                elif type(keyword.__dict__["value"]) == ast.Name:
                                    type_script_object.__dict__["keywords"]["id"] =  keyword.__dict__["value"].__dict__['id']
                                    

                        for arg in class_def.__dict__["value"].__dict__["args"]:
                            type_script_object.__dict__["args"].append(arg.__dict__["value"])
                        
                        
                        cls.attributes.append(type_script_object) 
                
                elif type(class_def) == ast.FunctionDef:
                    print(class_def)
            print(cls)

if __name__ == "__main__":
    test1()