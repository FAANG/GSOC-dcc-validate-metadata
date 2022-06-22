from graphene import ObjectType, String, relay
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

class AnalysisJoinField(ObjectType):
    experiment = relay.ConnectionField('graphql_api.grapheneObjects.experiment.schema.ExperimentConnection')