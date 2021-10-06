from django.shortcuts import render
from .models import Room
from .serializer import RoomSerialzier
from django.http import (JsonResponse, HttpResponseNotFound, HttpResponseServerError)
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt

from rest_framework.authentication import ( TokenAuthentication )
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import (api_view, authentication_classes, permission_classes)

from rest_framework_simplejwt.authentication import JWTAuthentication


# Create your views here.
@api_view(['GET'])
@authentication_classes([TokenAuthentication, JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_all_room(request) :
    if request.method == "GET" :
        rooms = Room.objects.all()
        print(request)
        serializer = RoomSerialzier(rooms, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == "POST" :
        data = JSONParser().parse(request)
        serializer = RoomSerialzier(data=data)
        if(serializer.is_valid()) :
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def get_room_detail(request, pk) :
    try : 
        room = Room.objects.filter(id=pk).first()
    except Room.DoesNotExist :
        return HttpResponseServerError()
    
    if request.method == "GET" :
        if room is None :
            return HttpResponseNotFound()
        else :
            serializer = RoomSerialzier(room)
            return JsonResponse(data=serializer.data, safe=False)
    elif request.method == "POST" :
        data = JSONParser().parse(request)
        serializer = RoomSerialzier(data=data)
        if(serializer.is_valid()) :
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


