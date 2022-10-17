from graphene import InputObjectType, ObjectType, String, Field,ID, relay, List, Int
from graphene.relay import Connection,Node
from graphql_api.tasks import resolve_all_task
from celery.result import AsyncResult


from .dataloader import SpecimenLoader

from ..helpers import resolve_all, resolve_single_document, resolve_with_join
from .fieldObjects import CellCulture_Field,SpecimenOrganism_Field,CellLine_Field,CellSpecimen_Field,SpecimenOrganization_Field,PoolOfSpecimens_Field,SpecimenPublishedArticles_Field,SpecimenCustomField_Field,SpecimenFromOrganism_Field,SpecimenJoin_Field
from .arguments.filter import SpecimenFilter_Argument
from ..commonFieldObjects import TextOntology_Field, TaskResponse

def resolve_single_specimen(args):
    q = ''

    if args['id']:
        id = args['id']
        q="biosampleId:{}".format(id)
    elif args['alternate_id']:
        alternate_id = args['alternate_id']
        q="alternateId:{}".format(alternate_id)
    res = resolve_single_document('specimen',q=q)
    # print(json.dumps(res,indent=4))
    res['id'] = res['biosampleId']
    return res


class SpecimenNode(ObjectType):
    class Meta:
        interfaces = (Node, )
    biosampleId = String()
    id_number = Int()
    alternativeId = String()
    etag = String()
    name = String()
    description = String()
    releaseDate = String()
    updateDate = String()
    standardMet = String()
    versionLastStandardMet = String()
    project = String()
    secondaryProject = String()
    organization = Field(SpecimenOrganization_Field)
    customField = Field(SpecimenCustomField_Field)
    material = Field(TextOntology_Field)
    derivedFrom = String()
    allDeriveFromSpecimens = String()
    availability = String()
    cellType = Field(TextOntology_Field)
    specimen = Field(SpecimenOrganism_Field)
    specimenFromOrganism = Field(SpecimenFromOrganism_Field)
    poolOfSpecimens = Field(PoolOfSpecimens_Field)
    cellSpecimen = Field(CellSpecimen_Field)
    cellCulture = Field(CellCulture_Field)
    cellLine = Field(CellLine_Field)
    paperPublished = String()
    publishedArticles = Field(SpecimenPublishedArticles_Field)
    trackhubUrl = String()
    join = Field(SpecimenJoin_Field)
    
    @classmethod
    def get_node(cls, info, id):
        args = {'id':id}
        return resolve_single_specimen(args)

class SpecimenConnection(Connection):
    class Meta:
        node = SpecimenNode
    
    class Edge:
        pass

specimenLoader = SpecimenLoader()

class SpecimenSchema(ObjectType):
    specimen = Field(SpecimenNode,id = ID(required=True), alternate_id = ID(required = False))
    # all_specimen = relay.ConnectionField(SpecimenConnection,filter=MyInputObjectType())
    all_specimens = relay.ConnectionField(SpecimenConnection,filter=SpecimenFilter_Argument())

    all_specimens_as_task = Field(TaskResponse,filter=SpecimenFilter_Argument())
    all_specimens_task_result = relay.ConnectionField(SpecimenConnection,task_id=String())
    # just an example of relay.connection field and batch loader
    some_specimens = relay.ConnectionField(SpecimenConnection,ids = List(of_type=String, required=True))

    def resolve_specimen(root,info,**args):
        return resolve_single_specimen(args)

    def resolve_all_specimens(root, info,**kwargs):
        filter_query = kwargs['filter'] if 'filter' in kwargs else {}
        res = resolve_with_join(filter_query,'specimen')
        return res

    def resolve_all_specimens_as_task(root, info,**kwargs):
        
        task = resolve_all_task.apply_async(args=[kwargs,'specimen'],queue='graphql_api')
        response = {'id':task.id,'status':task.status,'result':task.result}
        return response

    def resolve_all_specimens_task_result(root,info, **kwargs):
        task_id = kwargs['task_id']
        res = AsyncResult(task_id).result
        return res if res else []

    # just an example of relay.connection field and batch loader
    def resolve_some_specimens(root,info,**args):
        print(args)
        
        res = specimenLoader.load_many(args['ids'])
        
        return res 
        