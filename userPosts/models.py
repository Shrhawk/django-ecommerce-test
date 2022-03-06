from django.db import models
from userAuth.models import User
from django.utils.translation import gettext as _
import datetime


class Post(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateField(_("Date"), default=datetime.date.today)
    updated_at = models.DateField(_("Date"), default=datetime.date.today)


class PostLikes(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateField(_("Date"), default=datetime.date.today)
    updated_at = models.DateField(_("Date"), default=datetime.date.today)
