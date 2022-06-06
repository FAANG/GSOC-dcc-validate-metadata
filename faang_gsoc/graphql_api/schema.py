from graphene import Schema, ObjectType,String

# class Query():
#     pass
class Query(ObjectType):
    hello = String(default_value="Hi!")



schema = Schema(query=Query)