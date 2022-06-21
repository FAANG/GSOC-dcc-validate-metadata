from graphene import ObjectType, String

class FilesField(ObjectType):
    name = String()
    url = String()
    type = String()
    size = String()
    checksumMethod = String()
    checksum = String()


class AnalysisDateField(ObjectType):
    text = String()
    unit = String()

class AnalysisProtocolField(ObjectType):
    url = String()
    filename = String()

class AnalysisOrganismField(ObjectType):
    text = String()
    ontologyTerms = String()
