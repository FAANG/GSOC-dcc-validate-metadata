from graphene import ObjectType, String, Field,ID, relay, List
from graphene.relay import Connection,Node

from .dataloader import ExperimentLoader

from ..helpers import resolve_single_document, resolve_with_join
from .fieldObjects import BS_seq_Field,CAGE_seq_Field,ChIP_seq_DNA_binding_Field,ChIP_seq_input_DNA_Field,ATAC_seq_Field,ExperimentCustomField_Field,DNase_seq_Field, ExperimentJoinField,ExperimentalProtocol_Field,ExtractionProtocol_Field,Hi_C_Field,LibraryPreparationDate_Field,LibraryPreparationLocationLatitude_Field,LibraryPreparationLocationLongitude_Field,RNA_seq_Field,SamplingToPreparationInterval_Field,SequencingDate_Field,SequencingLocationLatitude_Field,SequencingLocationLongitude_Field,WGS_Field
from .arguments.filter import ExperimentFilter_Argument
def resolve_single_experiment(args):
    q = ''

    if args['id']:
        id = args['id']
        q="accession:{}".format(id)
    elif args['alternate_id']:
        alternate_id = args['alternate_id']
        q="alternateId:{}".format(alternate_id)
    res = resolve_single_document('experiment',q=q)
    # print(json.dumps(res,indent=4))
    res['id'] = res['accession']
    return res


class ExperimentNode(ObjectType):
    class Meta:
        interfaces = (Node, )

    accession = String()
    project = String()
    secondaryProject = String()
    assayType = String()
    experimentTarget = String()
    standardMet = String()
    versionLastStandardMet = String()
    libraryName = String()
    sampleStorage = String()
    sampleStorageProcessing = String()

    samplingToPreparationInterval = Field(SamplingToPreparationInterval_Field)
    
    experimentalProtocol = Field(ExperimentalProtocol_Field)
    extractionProtocol = Field(ExtractionProtocol_Field)


    libraryPreparationLocation = String()

    libraryPreparationLocationLatitude = Field(LibraryPreparationLocationLatitude_Field)
    
    libraryPreparationLocationLongitude = Field(LibraryPreparationLocationLongitude_Field)
    
    libraryPreparationDate = Field(LibraryPreparationDate_Field)
    
    sequencingLocation = String()

    sequencingLocationLongitude = Field(SequencingLocationLongitude_Field)
    sequencingLocationLatitude = Field(SequencingLocationLatitude_Field)
    
    sequencingDate = Field(SequencingDate_Field)
    
    customField = Field(ExperimentCustomField_Field)
    
    ATAC_seq = Field(ATAC_seq_Field)
    BS_seq = Field(BS_seq_Field)
    ChIP_seq_DNA_binding = Field(ChIP_seq_DNA_binding_Field)
    ChIP_seq_input_DNA = Field(ChIP_seq_input_DNA_Field)
    DNase_seq = Field(DNase_seq_Field)
    Hi_C = Field(Hi_C_Field)  
    RNA_seq = Field(RNA_seq_Field)
    WGS = Field(WGS_Field)
    CAGE_seq = Field(CAGE_seq_Field)  
    join = Field(ExperimentJoinField)
    
    @classmethod
    def get_node(cls, info, id):
        args = {'id':id}
        return resolve_single_experiment(args)

class ExperimentConnection(Connection):
    class Meta:
        node = ExperimentNode
    
    class Edge:
        pass

experimentLoader = ExperimentLoader()

class ExperimentSchema(ObjectType):
    experiment = Field(ExperimentNode,id = ID(required=True), alternate_id = ID(required = False))
    all_experiments = relay.ConnectionField(ExperimentConnection, filter=ExperimentFilter_Argument())

    # just an example of relay.connection field and batch loader
    some_experiments = relay.ConnectionField(ExperimentConnection,ids = List(of_type=String, required=True))

    def resolve_experiment(root,info,**args):
        return resolve_single_experiment(args)

    def resolve_all_experiments(root, info,**kwargs):
        filter_query = kwargs['filter'] if 'filter' in kwargs else {}
        res = resolve_with_join(filter_query,'experiment')
        return res

    # just an example of relay.connection field and batch loader
    def resolve_some_experiments(root,info,**args):
        print(args)
        
        res = experimentLoader.load_many(args['ids'])
        
        return res 
        