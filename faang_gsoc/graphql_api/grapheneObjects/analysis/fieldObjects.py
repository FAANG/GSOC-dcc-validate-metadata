from graphene import ObjectType, String, relay
class Files_Field(ObjectType):
    name = String()
    url = String()
    type = String()
    size = String()
    checksumMethod = String()
    checksum = String()


class AnalysisDate_Field(ObjectType):
    text = String()
    unit = String()

class AnalysisOrganism_Field(ObjectType):
    text = String()
    ontologyTerms = String()

class AnalysisJoin_Field(ObjectType):
    experiment = relay.ConnectionField('graphql_api.grapheneObjects.experiment.schema.ExperimentConnection')
    article = relay.ConnectionField('graphql_api.grapheneObjects.article.schema.ArticleConnection')
    dataset = relay.ConnectionField('graphql_api.grapheneObjects.dataset.schema.DatasetConnection')
    specimen = relay.ConnectionField('graphql_api.grapheneObjects.specimen.schema.SpecimenConnection')
    