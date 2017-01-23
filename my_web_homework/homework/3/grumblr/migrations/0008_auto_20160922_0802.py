# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-22 13:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0007_post_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='time',
            field=models.CharField(default='00:00', max_length=100),
        ),
        migrations.AlterField(
            model_name='post',
            name='user',
            field=models.CharField(max_length=50),
        ),
    ]