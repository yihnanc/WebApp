from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone

class Follow(models.Model):
    owner = models.OneToOneField(User)
    follow = models.ManyToManyField(User, related_name = 'following', symmetrical=False, blank = True)


class Profile(models.Model):
    owner = models.OneToOneField(User)
    bio = models.CharField(max_length=420, default="", blank=True)
    first_name = models.CharField(max_length=20, default="", blank=True)
    last_name = models.CharField(max_length=20, default="", blank=True)
    age = models.IntegerField(default=0, blank=True)
    picture = models.ImageField(upload_to="grumblr", blank=True)

class Post(models.Model):
    post = models.CharField(max_length=42)
    users = models.ForeignKey(User)
    time = models.CharField(max_length=100, default='00:00')
    created_date = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return '%s %s %s' % (self.post, self.users.username, self.time)

