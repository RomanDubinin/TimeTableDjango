from django.db import models
from django.contrib.auth.models import User
from django.conf import settings 

class UserSkif(models.Model):
    name = models.CharField(max_length=100)