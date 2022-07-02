from graphene import ObjectType, String, Field,ID, relay, List, Int
from graphene.relay import Connection,Node

from .dataloader import OrganismLoader

from ..helpers import resolve_all, resolve_with_join, resolve_single_document
from .fieldObjects import Organism_Field,OrganismCustomField_Field,BirthDate_Field,BirthLocationLatitude_Field,BirthLocationLongitude_Field,BirthWeight_Field,Breed_Field,HealthStatus_Field,Material_Field,FileOrganization_Field,PlacentalWeight_Field,PregnancyLength_Field,OrganismPublishedArticles_Field,Sex_Field, OrganismJoin_Field
from .arguments.filter import OrganismFilter_Argument
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
    organization = Field(FileOrganization_Field)
    customField = Field(OrganismCustomField_Field)
    material = Field(Material_Field)
    availability = String()
    organism = Field(Organism_Field)
    sex = Field(Sex_Field)
    breed = Field(Breed_Field)
    birthDate = Field(BirthDate_Field)
    healthStatus = Field(HealthStatus_Field)
    birthLocation = String()
    birthLocationLongitude = Field(BirthLocationLongitude_Field)
    birthLocationLatitude = Field(BirthLocationLatitude_Field)
    birthWeight = Field(BirthWeight_Field)
    placentalWeight = Field(PlacentalWeight_Field)
    pregnancyLength = Field(PregnancyLength_Field)
    deliveryTiming = String()
    deliveryEase = String()
    childOf = String()
    pedigree = String()
    paperPublished = String()
    publishedArticles = Field(OrganismPublishedArticles_Field)
    join = Field(OrganismJoin_Field)
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
    # all_organism = relay.ConnectionField(OrganismConnection,filter=MyInputObjectType())
    all_organisms = relay.ConnectionField(OrganismConnection,filter=OrganismFilter_Argument())

    # just an example of relay.connection field and batch loader
    some_organisms = relay.ConnectionField(OrganismConnection,ids = List(of_type=String, required=True))

    def resolve_organism(root,info,**args):
        return resolve_single_organism(args)

    def resolve_all_organisms(root, info,**kwargs):
        filter_query = kwargs['filter'] if 'filter' in kwargs else {}
        res = resolve_with_join(filter_query,'organism')
        return res

    # just an example of relay.connection field and batch loader
    def resolve_some_organisms(root,info,**args):
        print(args)
        
        res = organismLoader.load_many(args['ids'])
        
        return res 
        