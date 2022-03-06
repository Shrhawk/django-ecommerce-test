import datetime

from django.db import models
from django.utils.translation import gettext as _


class BaseModel(models.Model):
    is_active = models.BooleanField(default=True)
    created_at = models.DateField(_("Date"), default=datetime.date.today)
    updated_at = models.DateField(_("Date"), default=datetime.date.today)

    class Meta:
        abstract = True
