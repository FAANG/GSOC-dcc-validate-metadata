from graphene import InputObjectType, String, Field,List

class Experiments_InputField(InputObjectType):
    accession = List(String)
    sampleStorage = List(String)
    sampleStorageProcessing = List(String)


class ProtocolFilesFilterBasic_Argument(InputObjectType):
    name = List(String)
    experimentTarget = List(String)
    assayType = List(String)
    key = List(String)
    url = List(String)
    filename = List(String)
    experiments = Field(Experiments_InputField)
    

class ProtocolFilesFilterJoin_Argument(InputObjectType):
    file = Field('graphql_api.grapheneObjects.file.arguments.filter.FileFilter_Argument')


class ProtocolFilesFilter_Argument(InputObjectType):
    basic = Field(ProtocolFilesFilterBasic_Argument)
    join = Field(ProtocolFilesFilterJoin_Argument)