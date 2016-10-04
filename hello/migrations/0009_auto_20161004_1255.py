# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0008_auto_20161004_1207'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userskif',
            name='days',
        ),
        migrations.AddField(
            model_name='userskif',
            name='choises',
            field=models.CharField(max_length=1000, default='[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]'),
        ),
    ]
