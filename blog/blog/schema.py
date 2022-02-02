import graphene
from graphene_django import DjangoObjectType
from graphql_auth.schema import UserQuery, MeQuery
from core import schema as core_schema


#Query

class Query(UserQuery, MeQuery, core_schema.Query, graphene.ObjectType):
    pass
    
class Mutation(core_schema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)