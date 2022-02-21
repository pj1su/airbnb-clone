from django.db import models
from . import managers


class TimeStampedModel(models.Model):

    """ Time Stamped Model """

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = managers.CustomModelManager()  # manager추가 할때에는 model에 추가해야함

    class Meta:
        abstract = True
