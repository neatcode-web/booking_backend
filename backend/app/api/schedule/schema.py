import graphene
import datetime

from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from .models import ( Room, Schedule, Floor )
from django.db.models import When, F, Q, Count, IntegerField, Case

from graphql_jwt.decorators import login_required

from backend.app.api.member.schema import MemberType

from dateutil.parser import parse

class RoomType(DjangoObjectType) :
    class Meta:
        model = Room
        fields = "__all__"
        pass

    schedule_count_completed = graphene.Int()
    schedule_count_booked = graphene.Int()
    schedule_count_inmeeting = graphene.Int()

    def resolve_schedule_count_completed(self, info) :
        now = datetime.datetime.now()
        schedules = Schedule.objects.filter(room_id = self.id, end_date__lt=now)
        return schedules.count()

    def resolve_schedule_count_booked(self, info) :
        now = datetime.datetime.now()
        schedules = Schedule.objects.filter(room_id = self.id, start_date__gt=now)
        return schedules.count()

    def resolve_schedule_count_inmeeting(self, info) :
        now = datetime.datetime.now()
        schedules = Schedule.objects.filter(room_id = self.id, start_date__lte=now, end_date__gte=now)
        return schedules.count()

    pass

class ScheduleType (DjangoObjectType) :
    class Meta :
        model = Schedule
        fields = "__all__"
        pass
    pass

class RoomStatusUpdateMutation (graphene.Mutation) :
    class Arguments :
        id = graphene.Int(required=True)
        status = graphene.Boolean()
        pass
    success = graphene.Boolean()

    @classmethod
    @login_required
    def mutate(cls, root, info, id, status) :
        room = Room.objects.get(id=id)
        if room is not None :
            room.status = status
            room.save()
            return RoomStatusUpdateMutation(success=True)
        else :
            return RoomStatusUpdateMutation(success=False)
            pass
        pass
    pass

class RoomCreateMutation (graphene.Mutation) :
    class Arguments : 
        title = graphene.String(required=True)
        floor = graphene.Int()
        status = graphene.Boolean()
        points = graphene.String()
        pass

    success = graphene.Boolean()

    @classmethod
    @login_required
    def mutate(cls, root, info, title, floor, status, points) :
        f = Floor.FLOOR1
        if floor == 2 :
            f = Floor.FLOOR2
            pass
        room = Room.objects.create(title=title, floor=f, status=status, points=points, position_x=0, position_y=0)

        return RoomCreateMutation(success=True)


class BookMeetingMutation (graphene.Mutation) :
    class Arguments:
        start_date = graphene.String(required=True)
        end_date = graphene.String(required=True)
        room_id = graphene.Int()
        user_id = graphene.Int()
        pass
    success = graphene.Boolean()
    schedule = graphene.Field(ScheduleType)

    @classmethod
    @login_required
    def mutate(cls, root, info, start_date, end_date, room_id, user_id) :
        room = Room.objects.get(id=room_id)
        user = get_user_model().objects.get(id=user_id)
        startDateObj = parse(start_date) #datetime.datetime.strptime(start_date, '%Y-%m-%dT%H:%M')
        endDateObj = parse(end_date) #datetime.datetime.strptime(end_date, '%Y-%m-%dT%H:%M')
        schedule = Schedule.objects.create(start_date=startDateObj, end_date=endDateObj, room_id=room, user_id=user)
        
        return BookMeetingMutation(success=True, schedule=schedule)
    pass

class RemoveMeetingMutation (graphene.Mutation) :
    class Arguments : 
        id = graphene.Int()
        pass
    success = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, id) :
        Schedule.objects.get(id=id).delete()
        return RemoveMeetingMutation(success=True)
    pass

class Query(graphene.ObjectType) :
    all_rooms = graphene.List(RoomType)
    all_schedules = graphene.List(ScheduleType)
    get_available_rooms = graphene.List(RoomType, start_date=graphene.String(required=True), end_date=graphene.String(required=True))
    get_schedules_by_user = graphene.List(ScheduleType, userId=graphene.Int())
    get_users_with_schedule = graphene.List(MemberType, date=graphene.String(required=True))
    get_rooms_with_schedule = graphene.List(RoomType, date=graphene.DateTime(required=True))
    get_schedule = graphene.Field(ScheduleType, id=graphene.Int())
    get_room_detail = graphene.Field(RoomType, id=graphene.Int())

    @login_required
    def resolve_all_rooms(root, info) :
        return Room.objects.all().order_by('id')

    @login_required
    def resolve_all_schedules(root, info) :
        schedules = Schedule.objects.all()

        return schedules

    @login_required
    def resolve_get_available_rooms(root, info, start_date, end_date) :

        startDateObj = parse(start_date) #datetime.datetime.strptime(start_date, '%Y-%m-%dT%H:%M')
        endDateObj = parse(end_date) #datetime.datetime.strptime(end_date, '%Y-%m-%dT%H:%M')

        rooms = Room.objects.annotate(conflict_schedules = Count(
            # Case(
            #     When(schedule__start_date__lt=startDateObj, then=1),
            #     When(schedule__end_date__gt=endDateObj, then=1),
            #     When(schedule__start_date__gt=startDateObj, schedule__end_date__lt=endDateObj, then=1),
            #     output_field=IntegerField()
            # )
            'schedule__id',
            filter=(
                ( Q(schedule__end_date__gt=startDateObj) & Q(schedule__end_date__lt=endDateObj) )
                | ( Q(schedule__start_date__gt=startDateObj) & Q(schedule__start_date__lt=endDateObj) )
                | ( Q(schedule__start_date__lt=startDateObj) & Q(schedule__end_date__gt=endDateObj))
                    )
        )).filter(conflict_schedules=0)
        return rooms

    @login_required
    def resolve_get_schedules_by_user(root, info, userId) :
        schedules = Schedule.objects.filter(user_id=userId)
        return schedules

    @login_required
    def resolve_get_users_with_schedule(root, info, date) :
        dateObj = parse(date)
        nextDateObj = dateObj + datetime.timedelta(days=1)
        users = get_user_model().objects.filter(schedule__start_date__gt=dateObj, schedule__end_date__lt=nextDateObj)
        return users
    
    @login_required
    def resolve_get_rooms_with_schedule(root, info, date) :
        nextDateObj = date + datetime.timedelta(days=1)
        rooms = Room.objects.filter(schedule__start_date__gt=date, schedule__end_date__lt=nextDateObj)
        return rooms

    @login_required
    def resolve_get_schedule(root, info, id) :
        schedule = Schedule.objects.get(pk=id)
        return schedule
    
    @login_required
    def resolve_get_room_detail(root, info, id) : 
        room = Room.objects.get(pk=id)
        return room
    
    pass

class RoomMutation (graphene.ObjectType) :
    change_room_status = RoomStatusUpdateMutation.Field()
    book_meeting = BookMeetingMutation.Field()
    remove_meeting = RemoveMeetingMutation.Field()
    create_room = RoomCreateMutation.Field()
    pass