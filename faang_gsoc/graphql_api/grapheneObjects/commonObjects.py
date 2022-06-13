from graphene import ObjectType, String

class FieldDetails(ObjectType):
    text = String()
    ontologyTerms = String()
