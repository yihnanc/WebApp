# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-22 00:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0005_auto_20160921_2332'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='user',
            field=models.CharField(default='anonymous', max_length=50),
        ),
    ]
