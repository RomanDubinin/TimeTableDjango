from django.db import models
from django.contrib.auth.models import User
from django.conf import settings 

import json

class UserSkif(models.Model):
    name = models.CharField(max_length=100)
    days = models.CharField(max_length=1000, default='[]')

    def setdays(self, x):
        self.days = json.dumps(x)

    def getdays(self):
        return json.loads(self.days)