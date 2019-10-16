import graphene

import profiles.schema
import youths.schema
import consents.schema


class Query(profiles.schema.Query, youths.schema.Query, consents.schema.Query, graphene.ObjectType):
    pass


class Mutation(profiles.schema.Mutation, youths.schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
