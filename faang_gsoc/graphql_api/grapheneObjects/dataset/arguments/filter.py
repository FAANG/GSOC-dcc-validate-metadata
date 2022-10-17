from graphene import InputObjectType, String, Field,List
from ...commonInputFieldObject import TextOntology_InputField


class Specimen_InputField(InputObjectType):
    biosampleId = List(String)
    material = Field(TextOntology_InputField)
    cellType = Field(TextOntology_InputField)
    sex = Field(TextOntology_InputField)
    breed = Field(TextOntology_InputField)

class File_InputField(InputObjectType):
    url = List(String)
    name = List(String)
    fileId = List(String)
    experiment = List(String)
    type = List(String)
    size = List(String)
    readableSize = List(String)
    archive = List(String)
    readCount = List(String)
    baseCount = List(String)
    checksumMethod = List(String)
    checksum = List(String)
    

class DatasetExperiment_InputField(InputObjectType):
    accession = List(String)
    target = List(String)
    assayType = List(String)
    
class DatasetPublishedArticles_InputField(InputObjectType):
    articleId = List(String)
    title = List(String)
    year = List(String)
    journal = List(String)
    

class DatasetFilterBasic_Argument(InputObjectType):
    accession = List(String)
    standardMet = List(String)
    secondaryProject = List(String)
    title = List(String)
    alias = List(String)
    assayType = List(String)
    tech = List(String)
    secondaryAccession = List(String)
    archive = List(String)
    specimen = Field(Specimen_InputField)
    species = Field(TextOntology_InputField)
    releaseDate = List(String)
    updateDate = List(String)
    file = Field(File_InputField)
    experiment = Field(DatasetExperiment_InputField)
    instrument = List(String)
    centerName = List(String)
    paperPublished = List(String)
    publishedArticles = Field(DatasetPublishedArticles_InputField)
    submitterEmail = List(String)
    

class DatasetFilterJoin_Argument(InputObjectType):
    experiment = Field('graphql_api.grapheneObjects.experiment.arguments.filter.ExperimentFilter_Argument')
    article = Field('graphql_api.grapheneObjects.article.arguments.filter.ArticleFilter_Argument')
    analysis = Field('graphql_api.grapheneObjects.analysis.arguments.filter.AnalysisFilter_Argument')
    specimen = Field('graphql_api.grapheneObjects.specimen.arguments.filter.SpecimenFilter_Argument')
    file = Field('graphql_api.grapheneObjects.file.arguments.filter.FileFilter_Argument')
    

class DatasetFilter_Argument(InputObjectType):
    basic = Field(DatasetFilterBasic_Argument)
    join = Field(DatasetFilterJoin_Argument)