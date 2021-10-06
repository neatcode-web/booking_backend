from django.shortcuts import render
from django.http import (JsonResponse, HttpResponseNotFound, HttpResponseServerError, HttpResponse)
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import (IsAuthenticated, AllowAny)
from rest_framework.response import (Response)
from rest_framework.views import APIView
from rest_framework.decorators import (api_view, authentication_classes, permission_classes)
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token

from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.
@csrf_exempt
@permission_classes([AllowAny])
def login(request) :
    if request.method == "POST" :
        credential  = JSONParser().parse(request)
        username    =  credential['username']
        password    = credential['password']

        if '@' in username :
            kwargs = {'email': username}
        else :
            kwargs = {'username': username}

        try :
            user = get_user_model().objects.filter(**kwargs).first()
            if user is not None and user.check_password(password): 
                # token = Token.objects.get(user=user)
                # if token is not None : 
                #     token.delete()
                
                # token = Token.objects.create(user = user)

                # print(token)
                # return HttpResponse(token)
                token = RefreshToken.for_user(user=user)
                print(token.access_token)
                return HttpResponse(token.access_token)
            else:
                return HttpResponse('invalid')
        except User.DoesNotExist:
            return HttpResponseNotFound()

        return HttpResponse(content=email)
    else : 
        return HttpResponseNotFound('Get is not supported')
    
