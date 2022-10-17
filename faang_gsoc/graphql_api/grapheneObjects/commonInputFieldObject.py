from graphene import InputObjectType, List, String

class TextOntology_InputField(InputObjectType):
    text = List(String)
    ontologyTerms = List(String)
    
class TextUnit_InputField(InputObjectType):
    text = List(String)
    unit = List(String)

class Protocol_InputField(InputObjectType):
    url = List(String)
    filename = List(String)
