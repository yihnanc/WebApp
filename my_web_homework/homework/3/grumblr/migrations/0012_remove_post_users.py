# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-22 13:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0011_auto_20160922_0833'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='users',
        ),
    ]