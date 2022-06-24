from graphene import Field, ObjectType, String, relay

class SamplingToPreparationInterval_Field(ObjectType):
    text = String()
    unit = String()

class ExperimentalProtocol_Field(ObjectType):
    url = String()
    filename = String()

class ExtractionProtocol_Field(ObjectType):
    url = String()
    filename = String()


class LibraryPreparationLocationLongitude_Field(ObjectType):
    text = String()
    unit = String()

class LibraryPreparationLocationLatitude_Field(ObjectType):
    text = String()
    unit = String()

class LibraryPreparationDate_Field(ObjectType):
    text = String()
    unit = String()

class SequencingLocationLongitude_Field(ObjectType):
    text = String()
    unit = String()

class SequencingLocationLatitude_Field(ObjectType):
    text = String()
    unit = String()

class SequencingDate_Field(ObjectType):
    text = String()
    unit = String()

class ExperimentCustomField_Field(ObjectType):
    name = String()
    value = String()
    unit = String()
    ontologyTerms = String()

class Protocol_Field(ObjectType):
    url = String()
    filename = String()


class ATAC_seq_Field(ObjectType):
    transposaseProtocol = Field(Protocol_Field)

    
class BS_seq_Field(ObjectType):
    librarySelection = String()
    bisulfiteConversionProtocol = Field(Protocol_Field)
    pcrProductIsolationProtocol = Field(Protocol_Field)
    bisulfiteConversionPercent = String()
    restrictionEnzyme = String()
    maxFragmentSizeSelectionRange = String()
    minFragmentSizeSelectionRange = String()


class ChIP_seq_DNA_binding_Field(ObjectType):
    chipProtocol = Field(Protocol_Field)
    chipTarget = String()
    controlExperiment = String()
    chipAntibodyProvider = String()
    chipAntibodyCatalog = String()
    chipAntibodyLot = String()
    libraryGenerationMaxFragmentSizeRange = String()
    libraryGenerationMinFragmentSizeRange = String()

class ChIP_seq_input_DNA_Field(ObjectType):
    chipProtocol = Field(Protocol_Field)
    libraryGenerationMaxFragmentSizeRange = String()
    libraryGenerationMinFragmentSizeRange = String()

class DNase_seq_Field(ObjectType):
    dnaseProtocol = Field(Protocol_Field)
    
class Hi_C_Field(ObjectType):
    restrictionEnzyme = String()
    restrictionSite = String()
    hi_cProtocol = Field(Protocol_Field)

class RNA_seq_Field(ObjectType):
    rnaPreparation3AdapterLigationProtocol = Field(Protocol_Field)
    rnaPreparation5AdapterLigationProtocol = Field(Protocol_Field)
    libraryGenerationPcrProductIsolationProtocol = Field(Protocol_Field)
    preparationReverseTranscriptionProtocol = Field(Protocol_Field)
    libraryGenerationProtocol = Field(Protocol_Field)
    readStrand = String()
    rnaPurity260280ratio = String()
    rnaPurity260230ratio = String()
    rnaIntegrityNumber = String()

class WGS_Field(ObjectType):
    libraryGenerationPcrProductIsolationProtocol = Field(Protocol_Field)
    libraryGenerationProtocol = Field(Protocol_Field)
    librarySelection = String()
    
class CAGE_seq_Field(ObjectType):
    cageProtocol = Field(Protocol_Field)
    sequencingPrimerProvider = String()
    sequencingPrimerCatalog = String()
    sequencingPrimerLot = String()
    restrictionEnzymeTargetSequence = String()
    rnaPurity260280ratio = String()
    rnaPurity260230ratio = String()
    rnaIntegrityNumber = String()

class ExperimentJoinField(ObjectType):
    analysis = relay.ConnectionField('graphql_api.grapheneObjects.analysis.schema.AnalysisConnection')
