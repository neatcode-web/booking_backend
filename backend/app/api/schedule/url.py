from django.conf.urls import include, url
from django.urls import path
from .views import (
    get_all_room,
    get_room_detail
)


urlpatterns = [
    path('room/all', get_all_room),
    path('room/detail/<pk>', get_room_detail)
]