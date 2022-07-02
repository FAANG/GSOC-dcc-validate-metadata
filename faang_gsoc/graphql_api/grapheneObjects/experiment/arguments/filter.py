# TODO handle kebab case fields
from graphene import Field, String, InputObjectType, List
from ...commonInputFieldObject import Protocol_InputField, TextUnit_InputField

class CustomField_InputField(InputObjectType):
    name = String()
    value = String()
    unit = String()
    ontologyTerms = String()

class ATAC_seq_InputField(InputObjectType):
    transposaseProtocol = Field(Protocol_InputField)

    
class BS_seq_InputField(InputObjectType):
    librarySelection = String()
    bisulfiteConversionProtocol = Field(Protocol_InputField)
    pcrProductIsolationProtocol = Field(Protocol_InputField)
    bisulfiteConversionPercent = String()
    restrictionEnzyme = String()
    maxFragmentSizeSelectionRange = String()
    minFragmentSizeSelectionRange = String()


class ChIP_seq_DNA_binding_InputField(InputObjectType):
    chipProtocol = Field(Protocol_InputField)
    chipTarget = String()
    controlExperiment = String()
    chipAntibodyProvider = String()
    chipAntibodyCatalog = String()
    chipAntibodyLot = String()
    libraryGenerationMaxFragmentSizeRange = String()
    libraryGenerationMinFragmentSizeRange = String()

class ChIP_seq_input_DNA_InputField(InputObjectType):
    chipProtocol = Field(Protocol_InputField)
    libraryGenerationMaxFragmentSizeRange = String()
    libraryGenerationMinFragmentSizeRange = String()

class DNase_seq_InputField(InputObjectType):
    dnaseProtocol = Field(Protocol_InputField)
    
class Hi_C_InputField(InputObjectType):
    restrictionEnzyme = String()
    restrictionSite = String()
    hi_cProtocol = Field(Protocol_InputField)

class RNA_seq_InputField(InputObjectType):
    rnaPreparation3AdapterLigationProtocol = Field(Protocol_InputField)
    rnaPreparation5AdapterLigationProtocol = Field(Protocol_InputField)
    libraryGenerationPcrProductIsolationProtocol = Field(Protocol_InputField)
    preparationReverseTranscriptionProtocol = Field(Protocol_InputField)
    libraryGenerationProtocol = Field(Protocol_InputField)
    readStrand = String()
    rnaPurity260280ratio = String()
    rnaPurity260230ratio = String()
    rnaIntegrityNumber = String()

class WGS_InputField(InputObjectType):
    libraryGenerationPcrProductIsolationProtocol = Field(Protocol_InputField)
    libraryGenerationProtocol = Field(Protocol_InputField)
    librarySelection = String()
    
class CAGE_seq_InputField(InputObjectType):
    cageProtocol = Field(Protocol_InputField)
    sequencingPrimerProvider = String()
    sequencingPrimerCatalog = String()
    sequencingPrimerLot = String()
    restrictionEnzymeTargetSequence = String()
    rnaPurity260280ratio = String()
    rnaPurity260230ratio = String()
    rnaIntegrityNumber = String()


class ExperimentFilterBasic_Argument(InputObjectType):
    accession = List(String)
    accession = List(String)
    project = List(String)
    secondaryProject = List(String)
    assayType = List(String)
    experimentTarget = List(String)
    standardMet = List(String)
    versionLastStandardMet = List(String)
    libraryName = List(String)
    sampleStorage = List(String)
    sampleStorageProcessing = List(String)

    samplingToPreparationInterval = Field(TextUnit_InputField)
    
    experimentalProtocol = Field(Protocol_InputField)
    extractionProtocol = Field(Protocol_InputField)


    libraryPreparationLocation = List(String)

    libraryPreparationLocationLatitude = Field(TextUnit_InputField)
    
    libraryPreparationLocationLongitude = Field(TextUnit_InputField)
    
    libraryPreparationDate = Field(TextUnit_InputField)
    
    sequencingLocation = List(String)

    sequencingLocationLongitude = Field(TextUnit_InputField)
    sequencingLocationLatitude = Field(TextUnit_InputField)
    
    sequencingDate = Field(TextUnit_InputField)
    
    customField = Field(CustomField_InputField)
    
    ATAC_seq = Field(ATAC_seq_InputField)
    BS_seq = Field(BS_seq_InputField)
    ChIP_seq_DNA_binding = Field(ChIP_seq_DNA_binding_InputField)
    ChIP_seq_input_DNA = Field(ChIP_seq_input_DNA_InputField)
    DNase_seq = Field(DNase_seq_InputField)
    Hi_C = Field(Hi_C_InputField)  
    RNA_seq = Field(RNA_seq_InputField)
    WGS = Field(WGS_InputField)
    CAGE_seq = Field(CAGE_seq_InputField)  
    

class ExperimentFilterJoin_Argument(InputObjectType):
    analysis = Field('graphql_api.grapheneObjects.analysis.arguments.filter.AnalysisFilter_Argument')
    dataset = Field('graphql_api.grapheneObjects.dataset.arguments.filter.DatasetFilter_Argument')
    file = Field('graphql_api.grapheneObjects.file.arguments.filter.FileFilter_Argument')
    
class ExperimentFilter_Argument(InputObjectType):
    basic = Field(ExperimentFilterBasic_Argument)
    join = Field(ExperimentFilterJoin_Argument)