from graphene import ObjectType, String, relay

class Experiments_Field(ObjectType):
    accession = String()
    sampleStorage = String()
    sampleStorageProcessing = String()

class ProtocolFilesJoin_Field(ObjectType):
    file = relay.ConnectionField('graphql_api.grapheneObjects.file.schema.FileConnection')