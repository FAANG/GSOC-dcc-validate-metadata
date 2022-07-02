from graphene import InputObjectType, String, Field,List

class Analyses_InputField(InputObjectType):
    accession = String()
    organism = String()
    datasetAccession = String()
    analysisType = String()

class ProtocolAnalysisFilterBasic_Argument(InputObjectType):
    universityName = String()
    protocolDate = String()
    protocolName = String()
    key = String()
    url = String()
    analyses = Field(Analyses_InputField)

class ProtocolAnalysisFilterJoin_Argument(InputObjectType):
    analysis = Field('graphql_api.grapheneObjects.analysis.arguments.filter.AnalysisFilter_Argument')


class ProtocolAnalysisFilter_Argument(InputObjectType):
    basic = Field(ProtocolAnalysisFilterBasic_Argument)
    join = Field(ProtocolAnalysisFilterJoin_Argument)