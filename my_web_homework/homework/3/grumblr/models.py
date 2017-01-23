from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone

# Create your models here.
class Post(models.Model):
    post = models.CharField(max_length=42)
    users = models.ForeignKey(User)
    time = models.CharField(max_length=100, default='00:00')
    created_date = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return '%s %s %s' % (self.post, self.users.username, self.time)
