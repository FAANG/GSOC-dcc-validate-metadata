from graphene import InputObjectType, ObjectType, String, Field,ID, relay, List
from graphene.relay import Connection,Node

from .dataloader import DatasetLoader

from ..helpers import resolve_all, resolve_single_document, resolve_with_join
from .fieldObjects import DatasetJoin_Field,DatasetExperiment_Field,File_Field,DatasetPublishedArticles_Field,Specimen_Field
from .arguments.filter import DatasetFilter_Argument
from ..commonFieldObjects import TextOntology_Field
def resolve_single_dataset(args):
    q = ''

    if args['id']:
        id = args['id']
        q="accession:{}".format(id)
    elif args['alternate_id']:
        alternate_id = args['alternate_id']
        q="alternateId:{}".format(alternate_id)
    res = resolve_single_document('dataset',q=q)
    # print(json.dumps(res,indent=4))
    res['id'] = res['accession']
    return res


class DatasetNode(ObjectType):
    class Meta:
        interfaces = (Node, )

    accession = String()
    standardMet = String()
    secondaryProject = String()
    title = String()
    alias = String()
    assayType = String()
    tech = String()
    secondaryAccession = String()
    archive = String()
    specimen = Field(Specimen_Field)
    species = Field(TextOntology_Field)
    releaseDate = String()
    updateDate = String()
    file = Field(File_Field)
    experiment = List(DatasetExperiment_Field)
    instrument = String()
    centerName = String()
    paperPublished = String()
    publishedArticles = Field(DatasetPublishedArticles_Field)
    submitterEmail = String()
    join = Field(DatasetJoin_Field)

    @classmethod
    def get_node(cls, info, id):
        args = {'id':id}
        return resolve_single_dataset(args)

class DatasetConnection(Connection):
    class Meta:
        node = DatasetNode
    
    class Edge:
        pass

datasetLoader = DatasetLoader()

class DatasetSchema(ObjectType):
    dataset = Field(DatasetNode,id = ID(required=True), alternate_id = ID(required = False))
    # all_dataset = relay.ConnectionField(DatasetConnection,filter=MyInputObjectType())
    all_datasets = relay.ConnectionField(DatasetConnection,filter=DatasetFilter_Argument())

    # just an example of relay.connection field and batch loader
    some_datasets = relay.ConnectionField(DatasetConnection,ids = List(of_type=String, required=True))

    def resolve_dataset(root,info,**args):
        return resolve_single_dataset(args)

    def resolve_all_datasets(root, info,**kwargs):
        filter_query = kwargs['filter'] if 'filter' in kwargs else {}
        res = resolve_with_join(filter_query,'dataset')
        return res

    # just an example of relay.connection field and batch loader
    def resolve_some_datasets(root,info,**args):
        print(args)
        
        res = datasetLoader.load_many(args['ids'])
        
        return res 
        