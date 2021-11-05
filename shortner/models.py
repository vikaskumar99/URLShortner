from django.db import models
from django.conf import settings

from django.contrib.auth.models import User
User._meta.get_field('email')._unique = True

class Url(models.Model):
    link = models.CharField(max_length=10000)
    uuid = models.CharField(max_length=10)
    clicks = models.IntegerField(default=0)
    created_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
