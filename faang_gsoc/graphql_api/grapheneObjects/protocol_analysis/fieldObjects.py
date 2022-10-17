from graphene import ObjectType, String, relay

class Analyses_Field(ObjectType):
    accession = String()
    organism = String()
    datasetAccession = String()
    analysisType = String()

class ProtocolAnalysisJoin_Field(ObjectType):
    analysis = relay.ConnectionField('graphql_api.grapheneObjects.analysis.schema.AnalysisConnection')