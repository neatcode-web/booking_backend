import graphene
from graphene_django import DjangoObjectType

from graphql_jwt.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, Group

from graphql_jwt.decorators import login_required

from backend.app.api.authentication.models import Profile, Role
from backend.app.api.authentication.schema import ProfileType
from backend.app.api.schedule.models import Schedule 

class ScheduleType1 (DjangoObjectType) :
    class Meta :
        model = Schedule
        fields = "__all__"
        pass
    pass

class MemberType(DjangoObjectType) :
    class Meta :
        model = get_user_model()
        fields = "__all__"
        pass

    matched_schedules = graphene.List(ScheduleType1)
    profile = graphene.Field(ProfileType)

    def resolve_profile(self, info) :
        profile = Profile.objects.get(user=self)
        return profile

    def resolve_matched_schedules(self, info) :
        return Schedule.objects.all()

    pass

class MemberQuery (graphene.ObjectType) :
    all_members = graphene.List(MemberType)
    all_members_count = graphene.Int(offset=graphene.Int())
    def resolve_all_members(root, info) :
        members = get_user_model().objects.all().order_by('id')
        return members
    def resolve_all_members_count(root, info, offset) :
        return offset

class MemberCreateMutation (graphene.Mutation) :
    class Arguments :
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        role = graphene.Int()
        status = graphene.Boolean()
        pass
    success = graphene.Boolean()
    user = graphene.Field(MemberType)

    @classmethod
    def mutate(cls, root, info, username, email, password, role, status) :
        user = get_user_model().objects.create(username=username, email=email, password=password)
        user.is_active = status
        user.save()
        if role == 0 :
            Profile.objects.create(user=user, role=Role.Admin)
        else : 
            Profile.objects.create(user=user, role=Role.Agent)
            pass
        return MemberCreateMutation(success=True, user=user)

class MemberUpdateMutation (graphene.Mutation) :
    class Arguments :
        id = graphene.Int()
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        role = graphene.Int()
        status = graphene.Boolean()
        updatePassword = graphene.Boolean()
        pass
    success = graphene.Boolean()
    user = graphene.Field(MemberType)

    @classmethod
    def mutate(cls, root, info, id, username, email, password, role, status, updatePassword) :
        user = get_user_model().objects.get(id=id)
        user.username = username
        user.email = email
        user.is_active = status
        
        if(updatePassword == True) :
            user.set_password(password)
            pass

        if role == 0 :
            user.profile.role = Role.Admin
        else : 
            user.profile.role = Role.Agent
            pass
        user.profile.save()
        user.save()

        return MemberUpdateMutation(success=True, user=user)

class Query (MemberQuery, graphene.ObjectType):
    pass

class Mutation (graphene.ObjectType) :
    create_new_user = MemberCreateMutation.Field()
    update_user     = MemberUpdateMutation.Field()
    pass