from graphene import ObjectType, String, relay

class Species_Field(ObjectType):
    text = String()
    ontologyTerms = String()

class FileExperiment_Field(ObjectType):
    accession = String()
    target = String()
    assayType = String()
    standardMet = String()

class Study_Field(ObjectType):
    accession = String()
    alias = String()
    type = String()
    secondaryAccession = String()
    title = String()

class Run_Field(ObjectType):
    accession = String()
    alias = String()
    platform = String()
    instrument = String()
    centerName = String()
    sequencingDate = String()
    sequencingLocation = String()
    sequencingLatitude = String()
    sequencingLongitude = String()

class FilePublishedArticles_Field(ObjectType):
    articleId = String()
    title = String()
    year = String()
    journal = String()
    pubmedId = String()
    doi = String()

class FileJoin_Field(ObjectType):
    experiment = relay.ConnectionField('graphql_api.grapheneObjects.experiment.schema.ExperimentConnection')
    article = relay.ConnectionField('graphql_api.grapheneObjects.article.schema.ArticleConnection')
    dataset = relay.ConnectionField('graphql_api.grapheneObjects.dataset.schema.DatasetConnection')
    organism = relay.ConnectionField('graphql_api.grapheneObjects.organism.schema.OrganismConnection')
    specimen = relay.ConnectionField('graphql_api.grapheneObjects.specimen.schema.SpecimenConnection')
    protocol_files = relay.ConnectionField('graphql_api.grapheneObjects.protocol_files.schema.ProtocolFilesConnection')
    protocol_samples = relay.ConnectionField('graphql_api.grapheneObjects.protocol_samples.schema.ProtocolSamplesConnection')