from django.conf.urls import include, url
from django.urls import path
from .views import (
    login
)


urlpatterns = [
    path('login', login),
]