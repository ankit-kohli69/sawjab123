# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-27 16:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20170427_1637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='location',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]