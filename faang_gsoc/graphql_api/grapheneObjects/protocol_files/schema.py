from graphene import InputObjectType, ObjectType, String, Field,ID, relay, List
from graphene.relay import Connection,Node

from .dataloader import ProtocolFilesLoader

from ..helpers import resolve_all, resolve_single_document, resolve_with_join
from .fieldObjects import Experiments_Field, ProtocolFilesJoin_Field
from .arguments.filter import ProtocolFilesFilter_Argument
def resolve_single_protocol_file(args):
    q = ''

    if args['id']:
        id = args['id']
        q="key:{}".format(id)
    elif args['alternate_id']:
        alternate_id = args['alternate_id']
        q="alternateId:{}".format(alternate_id)
    res = resolve_single_document('protocol_files',q=q)
    # print(json.dumps(res,indent=4))
    res['id'] = res['key']
    return res


class ProtocolFilesNode(ObjectType):
    class Meta:
        interfaces = (Node, )

    name = String()
    experimentTarget = String()
    assayType = String()
    key = String()
    url = String()
    filename = String()
    experiments = Field(Experiments_Field)
    join = Field(ProtocolFilesJoin_Field)
    
    @classmethod
    def get_node(cls, info, id):
        args = {'id':id}
        return resolve_single_protocol_file(args)

class ProtocolFilesConnection(Connection):
    class Meta:
        node = ProtocolFilesNode
    
    class Edge:
        pass

protocolFilesLoader = ProtocolFilesLoader()

class ProtocolFilesSchema(ObjectType):
    protocol_file = Field(ProtocolFilesNode,id = ID(required=True), alternate_id = ID(required = False))
    # all_protocol_files = relay.ConnectionField(ProtocolFilesConnection,filter=MyInputObjectType())
    all_protocol_files = relay.ConnectionField(ProtocolFilesConnection,filter=ProtocolFilesFilter_Argument())

    # just an example of relay.connection field and batch loader
    some_protocol_files = relay.ConnectionField(ProtocolFilesConnection,ids = List(of_type=String, required=True))

    def resolve_protocol_file(root,info,**args):
        return resolve_single_protocol_file(args)

    def resolve_all_protocol_files(root, info,**kwargs):
        filter_query = kwargs['filter'] if 'filter' in kwargs else {}
        res = resolve_with_join(filter_query,'protocol_files')
        return res

    # just an example of relay.connection field and batch loader
    def resolve_some_protocol_files(root,info,**args):
        print(args)
        
        res = protocolFilesLoader.load_many(args['ids'])
        
        return res 
        