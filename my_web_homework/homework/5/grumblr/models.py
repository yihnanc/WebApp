from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone
from django.db.models import Max
from django.utils.html import escape
from itertools import chain
from operator import attrgetter

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
    #last_changed = models.DateTimeField(auto_now=True)

    def __unicode__(self):                                                  
        return '%s %s %s' % (self.post, self.time, self.users.username)
    def __str__(self):
        return self.__unicode__()

    # Returns all recent additions to the to-do list.
    @staticmethod
    def get_streams(time="1970-01-01T00:00+00:00"):
        return Post.objects.filter(created_date__gt=time).distinct()

    @staticmethod
    def get_userStreams(user, time="1970-01-01T00:00+00:00"):
        return Post.objects.filter(created_date__gt=time, users=user).distinct()

    @staticmethod
    def get_followerStreams(user, time="1970-01-01T00:00+00:00"):
        list_post=[]
        try:
            follower = Follow.objects.get(owner=user)
        except:
            return list_post
        setFollowers = list(follower.follow.all())
        for index in setFollowers:
            if list_post:
                current = Post.objects.filter(users=index, created_date__gt=time).distinct()
                list_post = sorted(chain(list_post, current), key=attrgetter('created_date'),reverse=True)
            else:    
                list_post = Post.objects.filter(users=index, created_date__gt=time).distinct()
        return list_post

    @property
    def html(self):
        return "</br><table id='item_%d' class='form-style-5'><div class='row'> <textarea class='textStyle1 textHeight textBackground' type='text' readonly='readonly' size='30' cols='50' row='3'>%s</textarea><br/><br/></div><div class='row'><div class='col-xs-2'><img src='/grumblr/photo/%s' width='50px'/><a href=/grumblr/%s><span class='userText'>%s</span></a></div><div class='col-xs-5'><input class='userText' type='text' value=%s></div></div><div class='row'><button class='btn btn-primary'>Comment</button><input class='textStyle1 textHeight' type='text' size='30' placeholder='Feedback something'></div></p></table>" % (self.id, escape(self.post), escape(self.users.username) ,escape(self.users.username) ,escape(self.users.username), escape(self.time))


    @staticmethod                                                           
    def get_max_time():
        return Post.objects.all().aggregate(Max('created_date'))['created_date__max'] or "1970-01-01T00:00+00:00"

class Comment(models.Model):
    comment = models.CharField(max_length=42)
    users = models.ForeignKey(User)
    postid = models.ForeignKey(Post)
    time = models.CharField(max_length=100, default='00:00')
    created_date = models.DateTimeField(default=timezone.now)

    def __unicode__(self):                                                  
        return '%s %s %s' % (self.comment, self.time, self.users.username)
    def __str__(self):
        return self.__unicode__()

    # Returns all recent additions to the to-do list.
    @staticmethod
    def get_comments(pid, time="1970-01-01T00:00+00:00"):
        return  Comment.objects.filter(created_date__gt=time, postid=pid).distinct()

    @property
    def html(self):
        return "<div class='row' id='item_%d'><div class='col-xs-2'><textarea class='textStyle3 textHeight textBackground1' type='text' readonly='readonly' size='30' cols='30' row='2'>%s</textarea><br/><br/></div></div><div class='row'><div class='col-xs-2'><img src='/grumblr/photo/%s' width='50px'/><a href=/grumblr/%s><span class='userText'>%s</span></a></div><div class='col-xs-6'><input class='userText textBackground' type='text' value=%s></div></div><div class='row'></div>" % (self.id, escape(self.comment), escape(self.users.username), escape(self.users.username) ,escape(self.users.username), escape(self.time))


    @staticmethod                                                           
    def get_max_time():
        return Comment.objects.all().aggregate(Max('created_date'))['created_date__max'] or "1970-01-01T00:00+00:00"




