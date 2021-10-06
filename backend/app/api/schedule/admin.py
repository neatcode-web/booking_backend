from django.contrib import admin

# Register your models here.
from .models import ( Room, Schedule )

admin.site.register(Room)
admin.site.register(Schedule)