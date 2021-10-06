"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from django.views.decorators.csrf import csrf_exempt

from graphene_django.views import GraphQLView
from .schema import schema

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import (api_view, authentication_classes, permission_classes)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('backend.app.api.authentication.url')),
    path('api/authenticated1/', include('backend.app.api.schedule.url')),

    path('api/graphql', 
        csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))
    )
]
