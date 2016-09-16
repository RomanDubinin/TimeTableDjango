from django.db import models
from django.contrib.auth.models import User
from django.conf import settings 

import json

from datetime import datetime

class UserSkif(models.Model):
    name = models.CharField(max_length=100)
    days = models.CharField(max_length=1000, default='[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]')
    last_works = models.CharField(max_length=100000, default='[]')

    def setdays(self, x):
        self.days = json.dumps(x)

    def getdays(self):
        return json.loads(self.days)

    def set_last_works(self, dates):
        strs = []
        for date in dates:
            strs.append(date.strftime("%Y-%m-%d"))
        self.last_works = json.dumps(strs)

    def get_last_works(self):
        dates = []
        strs = json.loads(self.last_works)

        for string in strs:
            dates.append(datetime.strptime(string, "%Y-%m-%d"))

        return dates