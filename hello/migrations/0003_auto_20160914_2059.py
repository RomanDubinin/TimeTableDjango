# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-14 15:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0002_auto_20160914_2049'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userskif',
            old_name='Name',
            new_name='name',
        ),
    ]