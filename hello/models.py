from django.db import models
from django.contrib.auth.models import User
from django.conf import settings 

import json

from datetime import datetime

class UserSkif(models.Model):
    name = models.CharField(max_length=100)
    choises = models.CharField(max_length=1000, default='[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]')
    last_works = models.CharField(max_length=100000, default='[]')

    def set_choises(self, x):
        self.choises = json.dumps(x)

    def get_choises(self):
        return json.loads(self.choises)

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

class StorableDate(models.Model):
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()