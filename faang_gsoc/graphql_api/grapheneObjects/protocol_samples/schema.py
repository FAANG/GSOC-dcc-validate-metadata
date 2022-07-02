from graphene import InputObjectType, ObjectType, String, Field,ID, relay, List
from graphene.relay import Connection,Node

from .dataloader import ProtocolSamplesLoader

from ..helpers import resolve_all, resolve_single_document, resolve_with_join
from .fieldObjects import ProtocolSamplesJoin_Field, Specimens_Field
from .arguments.filter import ProtocolSamplesFilter_Argument
def resolve_single_protocol_sample(args):
    q = ''

    if args['id']:
        id = args['id']
        q="key:{}".format(id)
    elif args['alternate_id']:
        alternate_id = args['alternate_id']
        q="alternateId:{}".format(alternate_id)
    res = resolve_single_document('protocol_samples',q=q)
    # print(json.dumps(res,indent=4))
    res['id'] = res['key']
    return res


class ProtocolSamplesNode(ObjectType):
    class Meta:
        interfaces = (Node, )

    universityName = String()
    protocolDate = String()
    protocolName = String()
    key = String()
    url = String()
    specimens = Field(Specimens_Field)
    join = Field(ProtocolSamplesJoin_Field)
    
    @classmethod
    def get_node(cls, info, id):
        args = {'id':id}
        return resolve_single_protocol_sample(args)

class ProtocolSamplesConnection(Connection):
    class Meta:
        node = ProtocolSamplesNode
    
    class Edge:
        pass

protocolSamplesLoader = ProtocolSamplesLoader()

class ProtocolSamplesSchema(ObjectType):
    protocol_sample = Field(ProtocolSamplesNode,id = ID(required=True), alternate_id = ID(required = False))
    # all_protocol_samples = relay.ConnectionField(ProtocolSamplesConnection,filter=MyInputObjectType())
    all_protocol_samples = relay.ConnectionField(ProtocolSamplesConnection,filter=ProtocolSamplesFilter_Argument())

    # just an example of relay.connection field and batch loader
    some_protocol_samples = relay.ConnectionField(ProtocolSamplesConnection,ids = List(of_type=String, required=True))

    def resolve_protocol_sample(root,info,**args):
        return resolve_single_protocol_sample(args)

    def resolve_all_protocol_samples(root, info,**kwargs):
        filter_query = kwargs['filter'] if 'filter' in kwargs else {}
        res = resolve_with_join(filter_query,'protocol_samples')
        return res

    # just an example of relay.connection field and batch loader
    def resolve_some_protocol_samples(root,info,**args):
        print(args)
        
        res = protocolSamplesLoader.load_many(args['ids'])
        
        return res 
        