from django.db import models
import datetime
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _


class User(AbstractUser):
    user_ip = models.CharField(max_length=30)
    holidays = models.JSONField(null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateField(_("Date"), default=datetime.date.today)
    updated_at = models.DateField(_("Date"), default=datetime.date.today)
