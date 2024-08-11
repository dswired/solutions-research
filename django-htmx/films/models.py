from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.functions import Lower

class User(AbstractUser):
    pass

class Film(models.Model):
    name = models.CharField(max_length=128, unique=True)
    users=models.ManyToManyField(User, related_name="films")

    class Meta:
        ordering = [Lower("name")]