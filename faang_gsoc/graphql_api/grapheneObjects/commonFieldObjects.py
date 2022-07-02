from graphene import ObjectType, String

class TextOntology_Field(ObjectType):
    text = String()
    ontologyTerms = String()
class TextUnit_Field(ObjectType):
    text = String()
    unit = String()

class Protocol_Field(ObjectType):
    url = String()
    filename = String()
