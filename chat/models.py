
from django.db import models
from django.contrib.auth.models import User


class Chat(models.Model):
    room_name = models.CharField(max_length=255)
    allowed_users = models.CharField(max_length=255)