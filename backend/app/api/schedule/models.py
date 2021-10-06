from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

# Create your models here.
class Floor(models.IntegerChoices) :
    FLOOR1 = 1
    FLOOR2 = 2

class Room(models.Model) :
    floor = models.IntegerField(choices=Floor.choices)
    position_x = models.IntegerField()
    position_y = models.IntegerField()
    title = models.CharField(max_length=100, blank=False)
    status = models.BooleanField(default=True)
    points = models.CharField(max_length=300, blank=True, null=True, default="")
    pass

class Schedule(models.Model) :
    start_date = models.DateTimeField(_(""), auto_now=False, auto_now_add=False)
    end_date = models.DateTimeField(_(""), auto_now=False, auto_now_add=False)

    user_id = models.ForeignKey(get_user_model(), verbose_name=_("user_id"), on_delete=models.CASCADE)
    room_id = models.ForeignKey(Room, verbose_name=_("room_id"), on_delete=models.CASCADE)
