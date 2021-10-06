from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
# Create your models here.

class Role(models.IntegerChoices):
    Admin = 1
    Agent = 2

class Profile(models.Model) :
    remember_token = models.CharField(max_length=250, blank=True, default="", null=True)
    remember_token_expire = models.DateTimeField(_(""), auto_now=False, auto_now_add=False, blank=True, null=True)
    role = models.IntegerField(choices=Role.choices)
    user = models.OneToOneField(
        get_user_model(),
        verbose_name=_("user_id"),
        on_delete=models.CASCADE,
        primary_key=True,
    )
    def __str__(self):
        return self.user.username