from django.db import models
from django.utils import timezone


class MyModelBase(models.Model):

    created_time = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True
