from graphene import ObjectType, String, relay, Field
from ..commonFieldObjects import Protocol_Field,TextOntology_Field,TextUnit_Field
class SpecimenOrganization_Field(ObjectType):
    name = String()
    role = String()
    URL = String()

class SpecimenCustomField_Field(ObjectType):
    name = String()
    value = String()
    unit = String()
    ontologyTerms = String()

class SpecimenOrganism_Field(ObjectType):
    biosampleId = String()
    organism = Field(TextOntology_Field)
    sex = Field(TextOntology_Field)
    breed = Field(TextOntology_Field)
    healthStatus = Field(TextOntology_Field)

class SpecimenFromOrganism_Field(ObjectType):
    specimenCollectionDate = Field(TextUnit_Field)
    animalAgeAtCollection = Field(TextUnit_Field)
    developmentalStage = Field(TextOntology_Field)
    healthStatusAtCollection = Field(TextOntology_Field)
    organismPart = Field(TextOntology_Field)
    specimenCollectionProtocol = Field(Protocol_Field)
    fastedStatus = String()
    numberOfPieces = Field(TextUnit_Field)
    specimenVolume = String()
    specimenSize = Field(TextUnit_Field)
    specimenWeight = Field(TextUnit_Field)
    specimenPictureUrl = String()
    gestationalAgeAtSampleCollection = Field(TextUnit_Field)

class PoolOfSpecimens_Field(ObjectType):
    poolCreationDate = Field(TextUnit_Field)
    poolCreationProtocol = Field(Protocol_Field)
    specimenVolume = Field(TextUnit_Field)
    specimenSize = Field(TextUnit_Field)
    specimenWeight = Field(TextUnit_Field)
    specimenPictureUrl = String()

class CellSpecimen_Field(ObjectType):
    markers = String()
    cellType = Field(TextOntology_Field)
    purificationProtocol = Field(Protocol_Field)

class CellCulture_Field(ObjectType):
    cultureType = Field(TextOntology_Field)
    cellType = Field(TextOntology_Field)
    cellCultureProtocol = Field(Protocol_Field)
    cultureConditions = String()
    numberOfPassages = String()

class CellLine_Field(ObjectType):
    organism = Field(TextOntology_Field)
    sex = Field(TextOntology_Field)
    cellLine = String()
    biomaterialProvider = String()
    catalogueNumber = String()
    numberOfPassages = String()
    dateEstablished = Field(TextUnit_Field)
    publication = String()
    breed = Field(TextOntology_Field)
    cellType = Field(TextOntology_Field)
    cultureConditions = String()
    cultureProtocol = Field(Protocol_Field)
    disease = Field(TextOntology_Field)
    karyotype = String()

class SpecimenPublishedArticles_Field(ObjectType):
    articleId = String()
    title = String()
    year = String()
    journal = String()
    pubmedId = String()
    doi = String()

  
class SpecimenJoin_Field(ObjectType):
    analysis = relay.ConnectionField('graphql_api.grapheneObjects.analysis.schema.AnalysisConnection')
    article = relay.ConnectionField('graphql_api.grapheneObjects.article.schema.ArticleConnection')
    dataset = relay.ConnectionField('graphql_api.grapheneObjects.dataset.schema.DatasetConnection')
    file = relay.ConnectionField('graphql_api.grapheneObjects.file.schema.FileConnection')
    organism = relay.ConnectionField('graphql_api.grapheneObjects.organism.schema.OrganismConnection')
    protocol_samples = relay.ConnectionField('graphql_api.grapheneObjects.protocol_samples.schema.ProtocolSamplesConnection')