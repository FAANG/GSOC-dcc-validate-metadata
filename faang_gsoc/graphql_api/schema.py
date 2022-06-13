from graphene import Schema, String,relay
from .tasks import graphql_task
from .grapheneObjects.helpers import resolve_all
from .grapheneObjects.organism.schema import OrganismSchema
class Query(OrganismSchema):
    hello = String()
    node = relay.Node.Field()

    def resolve_hello(parent,info):
        # res = graphql_task.apply_async(queue='graphql_q')
        res2 = resolve_all('organism')
        print(res2)
        # res = graphql_task.apply_async(queue='graphql_api')
        # print(res)
        return res2
        # return 'Hola'

schema = Schema(query=Query)