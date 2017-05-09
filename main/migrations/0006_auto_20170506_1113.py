# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-06 11:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20170506_1111'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answer',
            old_name='text',
            new_name='content',
        ),
        migrations.RemoveField(
            model_name='question',
            name='text',
        ),
        migrations.AddField(
            model_name='question',
            name='title',
            field=models.TextField(default=None),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='question',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
    ]
