from graphene import Schema, ObjectType,String
from .tasks import graphql_task

# class Query():
#     pass
class Query(ObjectType):
    hello = String()

    def resolve_hello(parent,info):
        # res = graphql_task.apply_async(queue='graphql_q')
        res = graphql_task.apply_async(queue='graphql_api')
        print(res)
        return 'Hola'

schema = Schema(query=Query)