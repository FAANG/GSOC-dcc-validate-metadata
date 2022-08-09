from graphene import Schema, String,relay, ObjectType, Field
from .tasks import graphql_task
from .grapheneObjects.helpers import resolve_all

from .grapheneObjects.organism.schema import OrganismSchema
from .grapheneObjects.analysis.schema import AnalysisSchema
from .grapheneObjects.experiment.schema import ExperimentSchema
from .grapheneObjects.dataset.schema import DatasetSchema
from .grapheneObjects.file.schema import FileSchema
from .grapheneObjects.article.schema import ArticleSchema
from .grapheneObjects.specimen.schema import SpecimenSchema
from .grapheneObjects.protocol_analysis.schema import ProtocolAnalysisSchema
from .grapheneObjects.protocol_samples.schema import ProtocolSamplesSchema
from .grapheneObjects.protocol_files.schema import ProtocolFilesSchema

class HelloObject(ObjectType):
    id = String()
    status = String()

class Query(OrganismSchema,ExperimentSchema, AnalysisSchema, ArticleSchema, DatasetSchema, FileSchema,SpecimenSchema, ProtocolAnalysisSchema, ProtocolFilesSchema, ProtocolSamplesSchema):
    hello = Field(HelloObject)
    node = relay.Node.Field()

    def resolve_hello(parent,info):
        
        args = ['one','two']
        task = graphql_task.apply_async(args=args,queue='graphql_api')
        response = {'id':task.id,'status':task.status}
        return response

schema = Schema(query=Query)