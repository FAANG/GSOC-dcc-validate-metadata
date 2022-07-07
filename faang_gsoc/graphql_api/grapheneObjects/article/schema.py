from graphene import ObjectType, String, Field,ID, relay, List
from graphene.relay import Connection,Node

from .dataloader import ArticleLoader

from ..helpers import resolve_all, resolve_single_document, resolve_with_join, sanitize_filter_basic_query
from .fieldObjects import RelatedDatasets_Field,ArticleJoin_Field
from .arguments.filter import ArticleFilter_Argument

class ArticleNode(ObjectType):
    class Meta:
        interfaces = (Node, )

    pmcId = String()
    pubmedId = String()
    doi = String()
    title = String()
    authorString = String()
    journal = String()
    issue = String()
    volume = String()
    year = String()
    pages = String()
    isOpenAccess = String()
    datasetSource = String()
    relatedDatasets = Field(RelatedDatasets_Field)
    secondaryProject = String()
    join = Field(ArticleJoin_Field)

    @classmethod
    def get_node(cls, info, id):
        args = {'id':id}
        return resolve_single_article(args)

class ArticleConnection(Connection):
    class Meta:
        node = ArticleNode
    
    class Edge:
        pass

articleLoader = ArticleLoader()

class ArticleSchema(ObjectType):
    article = Field(ArticleNode,id = ID(required=True), alternate_id = ID(required = False))
    # all_article = relay.ConnectionField(ArticleConnection,filter=MyInputObjectType())
    all_articles = relay.ConnectionField(ArticleConnection,filter=ArticleFilter_Argument())

    # just an example of relay.connection field and batch loader
    some_articles = relay.ConnectionField(ArticleConnection,ids = List(of_type=String, required=True))

    def resolve_article(root,info,**args):
        res = resolve_single_document('article',args['id'],['pmcId','pubmedId'])
        return res

    def resolve_all_articles(root, info,**kwargs):
        filter_query = kwargs['filter'] if 'filter' in kwargs else {}
        res = resolve_with_join(filter_query,'article')
        return res

    # just an example of relay.connection field and batch loader
    def resolve_some_articles(root,info,**args):
        print(args)
        
        res = articleLoader.load_many(args['ids'])
        
        return res 
        