from common.base_model import BaseModel
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser, BaseModel):
    user_ip = models.CharField(max_length=30)
    holidays = models.JSONField(null=True)
