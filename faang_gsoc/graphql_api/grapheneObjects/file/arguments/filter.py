from graphene import InputObjectType, String, Field,List


class Species_InputField(InputObjectType):
    text = List(String)
    ontologyTerms = List(String)

class FileExperiment_InputField(InputObjectType):
    accession = List(String)
    target = List(String)
    assayType = List(String)
    standardMet = List(String)

class Study_InputField(InputObjectType):
    accession = List(String)
    alias = List(String)
    type = List(String)
    secondaryAccession = List(String)
    title = List(String)

class Run_InputField(InputObjectType):
    accession = List(String)
    alias = List(String)
    platform = List(String)
    instrument = List(String)
    centerName = List(String)
    sequencingDate = List(String)
    sequencingLocation = List(String)
    sequencingLatitude = List(String)
    sequencingLongitude = List(String)

class FilePublishedArticles_InputField(InputObjectType):
    articleId = List(String)
    title = List(String)
    year = List(String)
    journal = List(String)
    pubmedId = List(String)
    doi = List(String)


class FileFilterBasic_Argument(InputObjectType):
    specimen = List(String)
    organism = List(String)
    species = Field(Species_InputField)
    url = List(String)
    name = List(String)
    secondaryProject = List(String)
    type = List(String)
    size = List(String)
    readableSize = List(String)
    checksum = List(String)
    checksumMethod = List(String)
    archive = List(String)
    readCount = List(String)
    baseCount = List(String)
    releaseDate = List(String)
    updateDate = List(String)
    submission = List(String)
    experiment = Field(FileExperiment_InputField)
    study = Field(Study_InputField)
    run = Field(Run_InputField)
    paperPublished = List(String)
    publishedArticles = Field(FilePublishedArticles_InputField)
    submitterEmail = List(String)
    
class FileFilterJoin_Argument(InputObjectType):
    experiment = Field('graphql_api.grapheneObjects.experiment.arguments.filter.ExperimentFilter_Argument')
    article = Field('graphql_api.grapheneObjects.article.arguments.filter.ArticleFilter_Argument')
    dataset = Field('graphql_api.grapheneObjects.dataset.arguments.filter.DatasetFilter_Argument')
    organism = Field('graphql_api.grapheneObjects.organism.arguments.filter.OrganismFilter_Argument')
    specimen = Field('graphql_api.grapheneObjects.specimen.arguments.filter.SpecimenFilter_Argument')
    protocol_files = Field('graphql_api.grapheneObjects.protocol_files.arguments.filter.ProtocolFilesFilter_Argument')
    protocol_samples = Field('graphql_api.grapheneObjects.protocol_samples.arguments.filter.ProtocolSamplesFilter_Argument')

class FileFilter_Argument(InputObjectType):
    basic = Field(FileFilterBasic_Argument)
    join = Field(FileFilterJoin_Argument)