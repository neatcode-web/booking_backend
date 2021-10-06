import graphene

from backend.app.api.schedule.schema import Query as ScheduleQuery
from backend.app.api.authentication.schema import Query as AuthQuery
from backend.app.api.member.schema import Query as MemberQuery

from backend.app.api.authentication.schema import AuthMutation
from backend.app.api.schedule.schema import RoomMutation
from backend.app.api.member.schema import Mutation as MemberMutation

class Query (ScheduleQuery, AuthQuery, MemberQuery, graphene.ObjectType) :
    pass

class Mutation (AuthMutation,RoomMutation, MemberMutation, graphene.ObjectType) :
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)