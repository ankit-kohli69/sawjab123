# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-02 10:46
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0003_auto_20170428_0712'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
            ],
        ),
        migrations.RenameField(
            model_name='answer',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='user_id',
            new_name='user',
        ),
        migrations.AddField(
            model_name='comment',
            name='answer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Answer'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='answer',
            name='comments',
            field=models.ManyToManyField(blank=True, related_name='answer_comments', through='main.Comment', to=settings.AUTH_USER_MODEL),
        ),
    ]
