# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-06 11:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20170506_1113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='title',
            field=models.CharField(max_length=150),
        ),
    ]