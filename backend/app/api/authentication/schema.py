import graphene
import uuid
from graphene_django import DjangoObjectType

from graphql_jwt.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, Group
import graphql_jwt

from graphql_jwt.shortcuts import create_refresh_token, get_token
from django.contrib.auth.models import User, update_last_login

from .mail import send_password_reset_mail
from .models import Profile

class ProfileType (DjangoObjectType) :
    class Meta :
        model = Profile
        fields = "__all__"
        pass

class UserType (DjangoObjectType) :
    class Meta :
        model = get_user_model()
        fields = "__all__"
        pass

    profile = graphene.Field(ProfileType)

    def resolve_profile(self, info) :
        profile = Profile.objects.get(user=self)
        return profile
    pass

class PermissionType (DjangoObjectType) :
    class Meta : 
        model = Permission
        fields = "__all__"
        pass
    pass

class GroupType (DjangoObjectType) :
    class Meta : 
        model = Group
        field = "__all__"
        pass
    pass

class SigninUser (graphene.Mutation) :
    class Arguments :
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        pass

    token = graphene.String()
    refresh_token = graphene.String()
    user = graphene.Field(UserType)

    @classmethod
    def mutate(cls, root, info, username, password) :
        if '@' in username :
            kwargs = {'email': username}
        else :
            kwargs = {'username': username}

        try :
            user = get_user_model().objects.filter(**kwargs).first()
            if user is not None and user.check_password(password): 
                token = get_token(user)
                refresh_token = create_refresh_token(user)
                update_last_login(None, user)
                return SigninUser(token=token, refresh_token=refresh_token, user=user)
            else:
                SigninUser(token="", user=None)
        except User.DoesNotExist:
            SigninUser(token="", user=None)

class ForgotPasswordMutation (graphene.Mutation) :
    class Arguments:
        username = graphene.String(required=True)
        pass

    success = graphene.Boolean()
    @classmethod
    def mutate(cls, root, info, username):
        if '@' in username :
            kwargs = {'email': username}
        else :
            kwargs = {'username': username}
        try :
            user = get_user_model().objects.filter(**kwargs).first()
            
            if user is not None :
                remember_token = uuid.uuid4()
                profile = user.profile
                if profile is None:
                    profile = Profile.object.create(user=user)
                profile.remember_token = remember_token
                profile.save()
                send_password_reset_mail(user.email, remember_token)
                return ForgotPasswordMutation(success=True)
            else:
                return ForgotPasswordMutation(success=False)
        except User.DoesNotExist:
            return ForgotPasswordMutation(success=False)

class ResetPasswordMutation (graphene.Mutation) :
    class Arguments:
        token=graphene.String(required=True)
        password = graphene.String(required=True)
        pass
    success = graphene.Boolean()
    @classmethod
    def mutate(cls, root, info, token, password):
        profile = Profile.objects.filter(remember_token=token).first()
        if profile is None:
            return ResetPasswordMutation(success=False)
        user = profile.user
        user.set_password(password)
        user.save()

        return ResetPasswordMutation(success=True)

class AuthMutation (graphene.ObjectType) :
    signin = SigninUser.Field()
    forgotPassword = ForgotPasswordMutation.Field()
    resetPassword = ResetPasswordMutation.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    revoke_token = graphql_jwt.Revoke.Field()
    pass

class Query (graphene.ObjectType) :
    pass