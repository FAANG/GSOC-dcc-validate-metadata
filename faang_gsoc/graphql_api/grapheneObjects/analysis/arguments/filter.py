from graphene import InputObjectType, String, Field

class Files_InputField(InputObjectType):
    name = String()
    url = String()
    type = String()
    size = String()
    checksumMethod = String()
    checksum = String()


class AnalysisDate_InputField(InputObjectType):
    text = String()
    unit = String()

class AnalysisProtocol_InputField(InputObjectType):
    url = String()
    filename = String()

class AnalysisOrganism_InputField(InputObjectType):
    text = String()
    ontologyTerms = String()

class AnalysisFilterBasic_Argument(InputObjectType):
    accession = String()
    project = String()
    secondaryProject = String()
    title = String()
    alias = String()
    description = String()
    standardMet = String()
    versionLastStandardMet = String()
    releaseDate = String()
    updateDate = String()
    organism = Field(AnalysisOrganism_InputField)
    type = String()
    datasetAccession = String()
    datasetInPortal = String()
    sampleAccessions = String()
    experimentAccessions = String()
    runAccessions = String()
    analysisAccessions = String()
    files = Field(Files_InputField)
    analysisDate = Field(AnalysisDate_InputField)
    assayType = String()
    analysisProtocol = Field(AnalysisProtocol_InputField)
    analysisType = String()
    referenceGenome = String()
    analysisCenter = String()
    analysisCodeRepository = String()
    experimentType = String()
    program = String()
    platform = String()
    imputation = String()
    

class AnalysisFilterJoin_Argument(InputObjectType):
    experiment = Field('graphql_api.grapheneObjects.experiment.arguments.filter.ExperimentFilter_Argument')


class AnalysisFilter_Argument(InputObjectType):
    basic = Field(AnalysisFilterBasic_Argument)
    join = Field(AnalysisFilterJoin_Argument)