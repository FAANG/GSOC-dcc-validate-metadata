from graphene import Schema, String,relay
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
class Query(OrganismSchema,ExperimentSchema, AnalysisSchema, ArticleSchema, DatasetSchema, FileSchema,SpecimenSchema, ProtocolAnalysisSchema, ProtocolFilesSchema, ProtocolSamplesSchema):
    hello = String()
    node = relay.Node.Field()

    def resolve_hello(parent,info):
        # res = graphql_task.apply_async(queue='graphql_q')
        res2 = resolve_all('organism')
        # print(res2)
        # res = graphql_task.apply_async(queue='graphql_api')
        # print(res)
        return res2
        # return 'Hola'

schema = Schema(query=Query)