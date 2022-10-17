from graphene import InputObjectType, ObjectType, String, Field,ID, relay, List
from graphene.relay import Connection,Node
from graphql_api.tasks import resolve_all_task
from celery.result import AsyncResult


from .dataloader import FileLoader

from ..helpers import getFileIndexPrimaryKeyFromName, resolve_all, resolve_single_document, resolve_with_join
from .fieldObjects import FileExperiment_Field,FileJoin_Field,FilePublishedArticles_Field,Run_Field,Species_Field,Study_Field
from .arguments.filter import FileFilter_Argument
from ..commonFieldObjects import TaskResponse


def resolve_single_file(args):
    q = ''


    if args['id']:
        id = args['id']
        q="_id:{}".format(id)
    elif args['alternate_id']:
        alternate_id = args['alternate_id']
        q="alternateId:{}".format(alternate_id)
    res = resolve_single_document('file',q=q)
    # print(json.dumps(res,indent=4))
    res['id'] = getFileIndexPrimaryKeyFromName(res['name'])
    return res


class FileNode(ObjectType):
    class Meta:
        interfaces = (Node, )

    specimen = String()
    organism = String()
    species = Field(Species_Field)
    url = String()
    name = String()
    secondaryProject = String()
    type = String()
    size = String()
    readableSize = String()
    checksum = String()
    checksumMethod = String()
    archive = String()
    readCount = String()
    baseCount = String()
    releaseDate = String()
    updateDate = String()
    submission = String()
    experiment = Field(FileExperiment_Field)
    study = Field(Study_Field)
    run = Field(Run_Field)
    paperPublished = String()
    publishedArticles = Field(FilePublishedArticles_Field)
    submitterEmail = String()
    join = Field(FileJoin_Field)
    
    @classmethod
    def get_node(cls, info, id):
        args = {'id':id}
        return resolve_single_file(args)

class FileConnection(Connection):
    class Meta:
        node = FileNode
    
    class Edge:
        pass

fileLoader = FileLoader()

class FileSchema(ObjectType):
    file = Field(FileNode,id = ID(required=True), alternate_id = ID(required = False))
    # all_file = relay.ConnectionField(FileConnection,filter=MyInputObjectType())
    all_files = relay.ConnectionField(FileConnection,filter=FileFilter_Argument())

    all_files_as_task = Field(TaskResponse,filter=FileFilter_Argument())
    all_files_task_result = relay.ConnectionField(FileConnection,task_id=String())
    # just an example of relay.connection field and batch loader
    some_files = relay.ConnectionField(FileConnection,ids = List(of_type=String, required=True))

    def resolve_file(root,info,**args):
        return resolve_single_file(args)

    def resolve_all_files(root, info,**kwargs):
        filter_query = kwargs['filter'] if 'filter' in kwargs else {}
        res = resolve_with_join(filter_query,'file')
        return res

    def resolve_all_files_as_task(root, info,**kwargs):
        
        task = resolve_all_task.apply_async(args=[kwargs,'file'],queue='graphql_api')
        response = {'id':task.id,'status':task.status,'result':task.result}
        return response

    def resolve_all_files_task_result(root,info, **kwargs):
        task_id = kwargs['task_id']
        res = AsyncResult(task_id).result
        return res if res else []

    # just an example of relay.connection field and batch loader
    def resolve_some_files(root,info,**args):
        print(args)
        
        res = fileLoader.load_many(args['ids'])
        
        return res 
        