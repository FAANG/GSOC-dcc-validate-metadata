from graphene import InputObjectType, String, Field,List

class RelatedDatasets_InputField(InputObjectType):
    accession = List(String)
    standardMet = List(String)
    species = List(String)


class ArticleFilterBasic_Argument(InputObjectType):
    pmcId = List(String)
    pubmedId = List(String)
    doi = List(String)
    title = List(String)
    authorString = List(String)
    journal = List(String)
    issue = List(String)
    volume = List(String)
    year = List(String)
    pages = List(String)
    isOpenAccess = List(String)
    datasetSource = List(String)
    relatedDatasets = Field(RelatedDatasets_InputField)
    secondaryProject = List(String)
    

class ArticleFilterJoin_Argument(InputObjectType):
    analysis = Field('graphql_api.grapheneObjects.analysis.arguments.filter.AnalysisFilter_Argument')
    dataset = Field('graphql_api.grapheneObjects.dataset.arguments.filter.DatasetFilter_Argument')
    file = Field('graphql_api.grapheneObjects.file.arguments.filter.FileFilter_Argument')
    specimen = Field('graphql_api.grapheneObjects.specimen.arguments.filter.SpecimenFilter_Argument')

class ArticleFilter_Argument(InputObjectType):
    basic = Field(ArticleFilterBasic_Argument)
    join = Field(ArticleFilterJoin_Argument)