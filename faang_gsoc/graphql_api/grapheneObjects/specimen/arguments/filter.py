from graphene import InputObjectType, String, Field,List, Int
from ...commonInputFieldObject import Protocol_InputField,TextOntology_InputField,TextUnit_InputField

class SpecimenOrganization_InputField(InputObjectType):
    name = List(String)
    role = List(String)
    URL = List(String)

class SpecimenCustomField_InputField(InputObjectType):
    name = List(String)
    value = List(String)
    unit = List(String)
    ontologyTerms = List(String)

class SpecimenOrganism_InputField(InputObjectType):
    biosampleId = List(String)
    organism = Field(TextOntology_InputField)
    sex = Field(TextOntology_InputField)
    breed = Field(TextOntology_InputField)
    healthStatus = Field(TextOntology_InputField)

class SpecimenFromOrganism_InputField(InputObjectType):
    specimenCollectionDate = Field(TextUnit_InputField)
    animalAgeAtCollection = Field(TextUnit_InputField)
    developmentalStage = Field(TextOntology_InputField)
    healthStatusAtCollection = Field(TextOntology_InputField)
    organismPart = Field(TextOntology_InputField)
    specimenCollectionProtocol = Field(Protocol_InputField)
    fastedStatus = List(String)
    numberOfPieces = Field(TextUnit_InputField)
    specimenVolume = List(String)
    specimenSize = Field(TextUnit_InputField)
    specimenWeight = Field(TextUnit_InputField)
    specimenPictureUrl = List(String)
    gestationalAgeAtSampleCollection = Field(TextUnit_InputField)

class PoolOfSpecimens_InputField(InputObjectType):
    poolCreationDate = Field(TextUnit_InputField)
    poolCreationProtocol = Field(Protocol_InputField)
    specimenVolume = Field(TextUnit_InputField)
    specimenSize = Field(TextUnit_InputField)
    specimenWeight = Field(TextUnit_InputField)
    specimenPictureUrl = List(String)

class CellSpecimen_InputField(InputObjectType):
    markers = List(String)
    cellType = Field(TextOntology_InputField)
    purificationProtocol = Field(Protocol_InputField)

class CellCulture_InputField(InputObjectType):
    cultureType = Field(TextOntology_InputField)
    cellType = Field(TextOntology_InputField)
    cellCultureProtocol = Field(Protocol_InputField)
    cultureConditions = List(String)
    numberOfPassages = List(String)

class CellLine_InputField(InputObjectType):
    organism = Field(TextOntology_InputField)
    sex = Field(TextOntology_InputField)
    cellLine = List(String)
    biomaterialProvider = List(String)
    catalogueNumber = List(String)
    numberOfPassages = List(String)
    dateEstablished = Field(TextUnit_InputField)
    publication = List(String)
    breed = Field(TextOntology_InputField)
    cellType = Field(TextOntology_InputField)
    cultureConditions = List(String)
    cultureProtocol = Field(Protocol_InputField)
    disease = Field(TextOntology_InputField)
    karyotype = List(String)

class SpecimenPublishedArticles_InputField(InputObjectType):
    articleId = List(String)
    title = List(String)
    year = List(String)
    journal = List(String)
    pubmedId = List(String)
    doi = List(String)

class SpecimenFilterBasic_Argument(InputObjectType):
    biosampleId = List(String)
    id_number = List(Int)
    alternativeId = List(String)
    etag = List(String)
    name = List(String)
    description = List(String)
    releaseDate = List(String)
    updateDate = List(String)
    standardMet = List(String)
    versionLastStandardMet = List(String)
    project = List(String)
    secondaryProject = List(String)
    organization = Field(SpecimenOrganization_InputField)
    customField = Field(SpecimenCustomField_InputField)
    material = Field(TextOntology_InputField)
    derivedFrom = List(String)
    allDeriveFromSpecimens = List(String)
    availability = List(String)
    cellType = Field(TextOntology_InputField)
    organism = Field(SpecimenOrganism_InputField)
    specimenFromOrganism = Field(SpecimenFromOrganism_InputField)
    poolOfSpecimens = Field(PoolOfSpecimens_InputField)
    cellSpecimen = Field(CellSpecimen_InputField)
    cellCulture = Field(CellCulture_InputField)
    cellLine = Field(CellLine_InputField)
    paperPublished = List(String)
    publishedArticles = Field(SpecimenPublishedArticles_InputField)
    trackhubUrl = List(String)
    

class SpecimenFilterJoin_Argument(InputObjectType):
    analysis = Field('graphql_api.grapheneObjects.analysis.arguments.filter.AnalysisFilter_Argument')
    article = Field('graphql_api.grapheneObjects.article.arguments.filter.ArticleFilter_Argument')
    dataset = Field('graphql_api.grapheneObjects.dataset.arguments.filter.DatasetFilter_Argument')
    file = Field('graphql_api.grapheneObjects.file.arguments.filter.FileFilter_Argument')
    organism = Field('graphql_api.grapheneObjects.organism.arguments.filter.OrganismFilter_Argument')
    protocol_samples = Field('graphql_api.grapheneObjects.protocol_samples.arguments.filter.ProtocolSamplesFilter_Argument')

class SpecimenFilter_Argument(InputObjectType):
    basic = Field(SpecimenFilterBasic_Argument)
    join = Field(SpecimenFilterJoin_Argument)