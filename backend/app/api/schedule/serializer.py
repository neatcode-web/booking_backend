from rest_framework import serializers 
from .models import (Room, Floor)

class RoomSerialzier(serializers.Serializer):
    floor = serializers.ChoiceField(choices=Floor)
    position_x = serializers.IntegerField()
    position_y = serializers.IntegerField()
    title = serializers.CharField()
    id = serializers.IntegerField(read_only=True)

    def create(self, validated_data):
        """
        Create and return a new `Room` instance, given the validated data.
        """
        return Room.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.floor = validated_data.get('floor', instance.floor)
        instance.position_x = validated_data.get('position_x', instance.position_x)
        instance.position_y = validated_data.get('position_y', instance.position_y)
        instance.title = validated_data.get('title', instance.title)
        return instance