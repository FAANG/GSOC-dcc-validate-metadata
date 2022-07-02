from graphene import InputObjectType, ObjectType, String, Field,ID, relay, List
from graphene.relay import Connection,Node

from .dataloader import AnalysisLoader

from ..helpers import resolve_all, resolve_single_document, resolve_with_join
from .fieldObjects import AnalysisDate_Field, AnalysisJoin_Field,Files_Field,AnalysisOrganism_Field
from .arguments.filter import AnalysisFilter_Argument
from ..commonFieldObjects import Protocol_Field
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
    organism = Field(AnalysisOrganism_Field)
    type = String()
    datasetAccession = String()
    datasetInPortal = String()
    sampleAccessions = String()
    experimentAccessions = String()
    runAccessions = String()
    analysisAccessions = String()
    files = Field(Files_Field)
    analysisDate = Field(AnalysisDate_Field)
    assayType = String()
    analysisProtocol = Field(Protocol_Field)
    analysisType = String()
    referenceGenome = String()
    analysisCenter = String()
    analysisCodeRepository = String()
    experimentType = String()
    program = String()
    platform = String()
    imputation = String()
    join = Field(AnalysisJoin_Field)
    
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
    # all_analysis = relay.ConnectionField(AnalysisConnection,filter=MyInputObjectType())
    all_analysis = relay.ConnectionField(AnalysisConnection,filter=AnalysisFilter_Argument())

    # just an example of relay.connection field and batch loader
    some_analysis = relay.ConnectionField(AnalysisConnection,ids = List(of_type=String, required=True))

    def resolve_analysis(root,info,**args):
        return resolve_single_analysis(args)

    def resolve_all_analysis(root, info,**kwargs):
        filter_query = kwargs['filter'] if 'filter' in kwargs else {}
        res = resolve_with_join(filter_query,'analysis')
        return res

    # just an example of relay.connection field and batch loader
    def resolve_some_analysis(root,info,**args):
        print(args)
        
        res = analysisLoader.load_many(args['ids'])
        
        return res 
        