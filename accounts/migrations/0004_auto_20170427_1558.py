# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-27 15:58
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20170427_1533'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='follow',
        ),
        migrations.AlterField(
            model_name='relationship',
            name='user_from',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='who', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='relationship',
            name='user_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='whom', to=settings.AUTH_USER_MODEL),
        ),
    ]