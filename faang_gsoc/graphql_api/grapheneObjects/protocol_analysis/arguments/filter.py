from graphene import InputObjectType, String, Field,List

class Analyses_InputField(InputObjectType):
    accession = List(String)
    organism = List(String)
    datasetAccession = List(String)
    analysisType = List(String)

class ProtocolAnalysisFilterBasic_Argument(InputObjectType):
    universityName = List(String)
    protocolDate = List(String)
    protocolName = List(String)
    key = List(String)
    url = List(String)
    analyses = Field(Analyses_InputField)

class ProtocolAnalysisFilterJoin_Argument(InputObjectType):
    analysis = Field('graphql_api.grapheneObjects.analysis.arguments.filter.AnalysisFilter_Argument')


class ProtocolAnalysisFilter_Argument(InputObjectType):
    basic = Field(ProtocolAnalysisFilterBasic_Argument)
    join = Field(ProtocolAnalysisFilterJoin_Argument)