from graphene import ObjectType, String, Field,ID, relay, List
from graphene.relay import Connection,Node

from .dataloader import OrganismLoader

from ..helpers import resolve_all, resolve_single_document
from ..commonObjects import FieldDetails

def resolve_single_organism(args):
    q = ''

    if args['id']:
        id = args['id']
        q="biosampleId:{}".format(id)
    elif args['alternate_id']:
        alternate_id = args['alternate_id']
        q="alternateId:{}".format(alternate_id)
    res = resolve_single_document('organism',q=q)
    # print(json.dumps(res,indent=4))
    res['id'] = res['biosampleId']
    return res


class OrganismNode(ObjectType):
    class Meta:
        interfaces = (Node, )

    biosampleId = String()
    breed = Field(FieldDetails)
    organism = Field(FieldDetails)
    sex = Field(FieldDetails)
    
    @classmethod
    def get_node(cls, info, id):
        args = {'id':id}
        return resolve_single_organism(args)

class OrganismConnection(Connection):
    class Meta:
        node = OrganismNode
    
    class Edge:
        pass

organismLoader = OrganismLoader()

class OrganismSchema(ObjectType):
    organism = Field(OrganismNode,id = ID(required=True), alternate_id = ID(required = False))
    all_organisms = relay.ConnectionField(OrganismConnection)
    some_organism = relay.ConnectionField(OrganismConnection,ids = List(of_type=String, required=True))

    def resolve_organism(root,info,**args):
        return resolve_single_organism(args)

    def resolve_all_organisms(root, info):
        return resolve_all('organism')

    # just an example of relay.connection field and batch loader
    def resolve_some_organism(root,info,**args):
        print(args)
        
        res = organismLoader.load_many(args['ids'])
        
        return res 
        