from graphene import InputObjectType, ObjectType, String, Field,ID, relay, List
from graphene.relay import Connection,Node
from graphql_api.tasks import resolve_all_task
from celery.result import AsyncResult

from .dataloader import AnalysisLoader

from ..helpers import resolve_all, resolve_single_document, resolve_with_join
from .fieldObjects import AnalysisDate_Field, AnalysisJoin_Field,Files_Field,AnalysisOrganism_Field
from .arguments.filter import AnalysisFilter_Argument
from ..commonFieldObjects import Protocol_Field, TaskResponse

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
    all_analysis_as_task = Field(TaskResponse,filter=AnalysisFilter_Argument())
    all_analysis_task_result = relay.ConnectionField(AnalysisConnection,task_id=String())
    # just an example of relay.connection field and batch loader
    some_analysis = relay.ConnectionField(AnalysisConnection,ids = List(of_type=String, required=True))

    def resolve_analysis(root,info,**args):
        return resolve_single_analysis(args)

    def resolve_all_analysis(root, info,**kwargs):
        
        filter_query = kwargs['filter'] if 'filter' in kwargs else {}
        res = resolve_with_join(filter_query,'analyis')
        return res

    def resolve_all_analysis_as_task(root, info,**kwargs):
        
        task = resolve_all_task.apply_async(args=[kwargs,'analysis'],queue='graphql_api')
        response = {'id':task.id,'status':task.status,'result':task.result}
        return response

    def resolve_all_analysis_task_result(root,info, **kwargs):
        task_id = kwargs['task_id']
        res = AsyncResult(task_id).result
        return res if res else []


    # just an example of relay.connection field and batch loader
    def resolve_some_analysis(root,info,**args):
        print(args)
        
        res = analysisLoader.load_many(args['ids'])
        
        return res 
        
    