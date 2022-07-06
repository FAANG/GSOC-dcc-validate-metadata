from graphene import InputObjectType, String, Field,List
from ...commonInputFieldObject import Protocol_InputField
class Files_InputField(InputObjectType):
    name = List(String)
    url = List(String)
    type = List(String)
    size = List(String)
    checksumMethod = List(String)
    checksum = List(String)


class AnalysisDate_InputField(InputObjectType):
    text = List(String)
    unit = List(String)

class AnalysisOrganism_InputField(InputObjectType):
    text = List(String)
    ontologyTerms = List(String)

class AnalysisFilterBasic_Argument(InputObjectType):
    accession = List(String)
    project = List(String)
    secondaryProject = List(String)
    title = List(String)
    alias = List(String)
    description = List(String)
    standardMet = List(String)
    versionLastStandardMet = List(String)
    releaseDate = List(String)
    updateDate = List(String)
    organism = Field(AnalysisOrganism_InputField)
    type = List(String)
    datasetAccession = List(String)
    datasetInPortal = List(String)
    sampleAccessions = List(String)
    experimentAccessions = List(String)
    runAccessions = List(String)
    analysisAccessions = List(String)
    files = Field(Files_InputField)
    analysisDate = Field(AnalysisDate_InputField)
    assayType = List(String)
    analysisProtocol = Field(Protocol_InputField)
    analysisType = List(String)
    referenceGenome = List(String)
    analysisCenter = List(String)
    analysisCodeRepository = List(String)
    experimentType = List(String)
    program = List(String)
    platform = List(String)
    imputation = List(String)
    

class AnalysisFilterJoin_Argument(InputObjectType):
    experiment = Field('graphql_api.grapheneObjects.experiment.arguments.filter.ExperimentFilter_Argument')
    article = Field('graphql_api.grapheneObjects.article.arguments.filter.ArticleFilter_Argument')
    dataset = Field('graphql_api.grapheneObjects.dataset.arguments.filter.DatasetFilter_Argument')
    specimen = Field('graphql_api.grapheneObjects.specimen.arguments.filter.SpecimenFilter_Argument')
    

class AnalysisFilter_Argument(InputObjectType):
    basic = Field(AnalysisFilterBasic_Argument)
    join = Field(AnalysisFilterJoin_Argument)