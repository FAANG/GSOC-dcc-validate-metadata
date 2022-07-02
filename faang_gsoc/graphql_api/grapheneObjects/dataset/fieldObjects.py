from graphene import ObjectType, String, relay, Field
from ..commonFieldObjects import TextOntology_Field

class Specimen_Field(ObjectType):
    biosampleId = String()
    material = Field(TextOntology_Field)
    cellType = Field(TextOntology_Field)
    organism = Field(TextOntology_Field)
    sex = Field(TextOntology_Field)
    breed = Field(TextOntology_Field)

class File_Field(ObjectType):
    url = String()
    name = String()
    fileId = String()
    experiment = String()
    type = String()
    size = String()
    readableSize = String()
    archive = String()
    readCount = String()
    baseCount = String()
    checksumMethod = String()
    checksum = String()
    

class DatasetExperiment_Field(ObjectType):
    accession = String()
    target = String()
    assayType = String()
    
class DatasetPublishedArticles_Field(ObjectType):
    articleId = String()
    title = String()
    year = String()
    journal = String()
    

class DatasetJoin_Field(ObjectType):
    experiment = relay.ConnectionField('graphql_api.grapheneObjects.experiment.schema.ExperimentConnection')
    article = relay.ConnectionField('graphql_api.grapheneObjects.article.schema.ArticleConnection')
    analysis = relay.ConnectionField('graphql_api.grapheneObjects.analysis.schema.AnalysisConnection')
    organism = relay.ConnectionField('graphql_api.grapheneObjects.organism.schema.OrganismConnection')
    specimen = relay.ConnectionField('graphql_api.grapheneObjects.specimen.schema.SpecimenConnection')
    file = relay.ConnectionField('graphql_api.grapheneObjects.file.schema.FileConnection')
    