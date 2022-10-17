from graphene import InputObjectType, String, Field,List

class Specimens_InputField(InputObjectType):
    id = List(String)
    organismPartCellType = List(String)
    organism = List(String)
    breed = List(String)
    derivedFrom = List(String)


class ProtocolSamplesFilterBasic_Argument(InputObjectType):
    universityName = List(String)
    protocolDate = List(String)
    protocolName = List(String)
    key = List(String)
    url = List(String)
    specimens = Field(Specimens_InputField)

class ProtocolSamplesFilterJoin_Argument(InputObjectType):
    organism = Field('graphql_api.grapheneObjects.organism.arguments.filter.OrganismFilter_Argument')
    specimen = Field('graphql_api.grapheneObjects.specimen.arguments.filter.SpecimenFilter_Argument')
    file = Field('graphql_api.grapheneObjects.file.arguments.filter.FileFilter_Argument')
    

class ProtocolSamplesFilter_Argument(InputObjectType):
    basic = Field(ProtocolSamplesFilterBasic_Argument)
    join = Field(ProtocolSamplesFilterJoin_Argument)