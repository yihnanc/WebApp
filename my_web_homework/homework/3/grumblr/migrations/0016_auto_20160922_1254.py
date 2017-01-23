# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-22 17:54
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0015_auto_20160922_1252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='users',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
