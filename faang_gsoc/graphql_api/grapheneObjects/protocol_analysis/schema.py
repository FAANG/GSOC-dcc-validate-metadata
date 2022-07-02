from graphene import InputObjectType, ObjectType, String, Field,ID, relay, List
from graphene.relay import Connection,Node

from .dataloader import ProtocolAnalysisLoader

from ..helpers import resolve_all, resolve_single_document, resolve_with_join
from .fieldObjects import Analyses_Field, ProtocolAnalysisJoin_Field
from .arguments.filter import ProtocolAnalysisFilter_Argument
def resolve_single_protocol_analysis(args):
    q = ''

    if args['id']:
        id = args['id']
        q="key:{}".format(id)
    elif args['alternate_id']:
        alternate_id = args['alternate_id']
        q="alternateId:{}".format(alternate_id)
    res = resolve_single_document('protocol_analysis',q=q)
    # print(json.dumps(res,indent=4))
    res['id'] = res['key']
    return res


class ProtocolAnalysisNode(ObjectType):
    class Meta:
        interfaces = (Node, )

    universityName = String()
    protocolDate = String()
    protocolName = String()
    key = String()
    url = String()
    analyses = Field(Analyses_Field)
    join = Field(ProtocolAnalysisJoin_Field)
    
    @classmethod
    def get_node(cls, info, id):
        args = {'id':id}
        return resolve_single_protocol_analysis(args)

class ProtocolAnalysisConnection(Connection):
    class Meta:
        node = ProtocolAnalysisNode
    
    class Edge:
        pass

protocolAnalysisLoader = ProtocolAnalysisLoader()

class ProtocolAnalysisSchema(ObjectType):
    protocol_analysis = Field(ProtocolAnalysisNode,id = ID(required=True), alternate_id = ID(required = False))
    # all_protocol_analysis = relay.ConnectionField(ProtocolAnalysisConnection,filter=MyInputObjectType())
    all_protocol_analysis = relay.ConnectionField(ProtocolAnalysisConnection,filter=ProtocolAnalysisFilter_Argument())

    # just an example of relay.connection field and batch loader
    some_protocol_analysis = relay.ConnectionField(ProtocolAnalysisConnection,ids = List(of_type=String, required=True))

    def resolve_protocol_analysis(root,info,**args):
        return resolve_single_protocol_analysis(args)

    def resolve_all_protocol_analysis(root, info,**kwargs):
        filter_query = kwargs['filter'] if 'filter' in kwargs else {}
        res = resolve_with_join(filter_query,'protocol_analysis')
        return res

    # just an example of relay.connection field and batch loader
    def resolve_some_protocol_analysis(root,info,**args):
        print(args)
        
        res = protocolAnalysisLoader.load_many(args['ids'])
        
        return res 
        