from graphene import ObjectType, String, Field,ID, relay, List, Int
from graphene.relay import Connection,Node

from .dataloader import AnalysisLoader

from ..helpers import resolve_all, resolve_single_document
from .fieldObjects import AnalysisDateField, AnalysisProtocolField,FilesField,AnalysisOrganismField

def resolve_single_analysis(args):
    q = ''

    if args['id']:
        id = args['id']
        q="accession:{}".format(id)
    elif args['alternate_id']:
        alternate_id = args['alternate_id']
        q="alternateId:{}".format(alternate_id)
    res = resolve_single_document('analysis',q=q)
    # print(json.dumps(res,indent=4))
    res['id'] = res['accession']
    return res


class AnalysisNode(ObjectType):
    class Meta:
        interfaces = (Node, )

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
    organism = Field(AnalysisOrganismField)
    type = String()
    datasetAccession = String()
    datasetInPortal = String()
    sampleAccessions = String()
    experimentAccessions = String()
    runAccessions = String()
    analysisAccessions = String()
    files = Field(FilesField)
    analysisDate = Field(AnalysisDateField)
    assayType = String()
    analysisProtocol = Field(AnalysisProtocolField)
    analysisType = String()
    referenceGenome = String()
    analysisCenter = String()
    analysisCodeRepository = String()
    experimentType = String()
    program = String()
    platform = String()
    imputation = String()

    @classmethod
    def get_node(cls, info, id):
        args = {'id':id}
        return resolve_single_analysis(args)

class AnalysisConnection(Connection):
    class Meta:
        node = AnalysisNode
    
    class Edge:
        pass

analysisLoader = AnalysisLoader()

class AnalysisSchema(ObjectType):
    analysis = Field(AnalysisNode,id = ID(required=True), alternate_id = ID(required = False))
    all_analysis = relay.ConnectionField(AnalysisConnection)

    # just an example of relay.connection field and batch loader
    some_analysis = relay.ConnectionField(AnalysisConnection,ids = List(of_type=String, required=True))

    def resolve_analysis(root,info,**args):
        return resolve_single_analysis(args)

    def resolve_all_analysis(root, info):
        return resolve_all('analysis')

    # just an example of relay.connection field and batch loader
    def resolve_some_analysis(root,info,**args):
        print(args)
        
        res = analysisLoader.load_many(args['ids'])
        
        return res 
        